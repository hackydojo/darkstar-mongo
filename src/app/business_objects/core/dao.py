from abc import abstractmethod, ABCMeta
from typing import List, Dict

from fastapi import HTTPException, status
from pymongo.errors import (
    AutoReconnect,
    BulkWriteError,
    CollectionInvalid,
    ConfigurationError,
    ConnectionFailure,
    CursorNotFound,
    DocumentTooLarge,
    DuplicateKeyError,
    EncryptionError,
    ExecutionTimeout,
    InvalidName,
    InvalidOperation,
    InvalidURI,
    NetworkTimeout,
    PyMongoError,
    WriteError,
    WriteConcernError,
)

from app.context import get_context, ServerContext
import functools


# =========================================================
# DECORATOR INJECT MONGO ERROR HANDLING
# =========================================================
def inject_mongodb_error_handling(func):
    """
    Decorator that centralizes and provides proper error
    handling and logging for every single Mongo operation
    without duplicating error handling code across  all
    service methods
    :param func: functions to be wrapped
    :return:
    """
    logging = get_context().logging

    @functools.wraps(func)
    def error_handling_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError as ie:
            logging.error(str(ie))
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except NetworkTimeout as nt:
            logging.error(str(nt))
        except AutoReconnect as ar:
            logging.error(str(ar))
        except BulkWriteError as bwe:
            if bwe.timeout:
                logging.error(str(bwe))
            logging.error(str(bwe))
        except CollectionInvalid as collection_invalid_error:
            logging.error(str(collection_invalid_error))
        except InvalidURI as invalid_url_error:
            logging.error(str(invalid_url_error))
        except ConfigurationError as configuration_error:
            logging.error(str(configuration_error))
        except ConnectionFailure as connection_failure_error:
            logging.error(str(connection_failure_error))
        except CursorNotFound as cursor_not_found_error:
            logging.error(str(cursor_not_found_error))
        except DocumentTooLarge as document_too_large_error:
            logging.error(str(document_too_large_error))
        except DuplicateKeyError as duplicated_key_error:
            logging.error(str(duplicated_key_error))
        except EncryptionError as ece:
            logging.error(str(ece.cause))
        except ExecutionTimeout as timeout_error:
            logging.error(str(timeout_error))
        except InvalidName as invalid_name_error:
            logging.error(str(invalid_name_error))
        except InvalidOperation as invalid_operation_error:
            logging.error(str(invalid_operation_error))
        except PyMongoError as pymongo_error:
            logging.error(str(pymongo_error))
        except WriteConcernError as write_concern_error:
            logging.error(str(write_concern_error))
        except WriteError as write_error:
            logging.error(str(write_error))
        except Exception as error:
            logging.error(str(error))
        return False

    return error_handling_wrapper


# =========================================================
# CLASS HEIMDALL ENTITY REPOSITORY
# =========================================================
class EntityRepository:
    __metaclass__ = ABCMeta

    def __init__(self, collection_name: str, context: ServerContext = get_context()):
        """
        EntityRepository is not designed to be instantiated
        directly because it is an abstract class. This class
        provides a set of generic _operations on top of
        Mongo Database Client. Specific actions should
        be implemented in classes that extend this class.

        :param collection_name: Name of the MongoDB Collection
        :param context: Shared worker context that provides access to
        database connection parameters and dependency inversion
        """
        self.db = context.database
        self.entities = self.db[collection_name]
        self.collection_name = collection_name
        self.context: ServerContext = context

    # -----------------------------------------------------
    # TRAVERSE CURSOR AND COPY
    # -----------------------------------------------------
    @staticmethod
    def traverse_cursor_and_copy(cursor):
        """
        Helper function that creates a local copy in-memory
        of the results obtained after traversing a cursor
        that is created as a result of a query with high
        projection. This enables data transformations on the
        results without losing the state of the returned
        documents.

        :param cursor: Iterable cursor that points to the
        results from the query.
        :return: A local copy (stored in Heap memory segment)
        of results (List of dictionaries).
        """
        result_set: list = []
        for result in cursor:
            result_set.append(result.copy())
        return result_set

    # -----------------------------------------------------
    # METHOD GET
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def get(self, query: Dict):
        """
        Get a set of documents on the given collection based
        on a filter (represented in Python as a dictionary).

        :param query: A dictionary containing a valid MongoDB
        filter
        :return: Local copy of results
        """
        return self.traverse_cursor_and_copy(
            self.entities.find(query).limit(self.context.query_limit)
        )

    # -----------------------------------------------------
    # METHOD GET BY ID
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def get_by_id(self, issue_id: str) -> Dict or None:
        """
        Given an issue_id (Internal unique identifier for
        ControlDB), it gets the entity with matching id if it
        exists
        :param issue_id: Unique ControlDB identifier for the
        entity
        :return: Dict if entity exists or None if not found
        """
        return self.get({"id": issue_id}).pop()

    # -----------------------------------------------------
    # METHOD UPDATE ONE
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def update_one(self, issue_id: str, new_values: dict):
        return self.entities.update_one({"id": issue_id}, {"$set": new_values})

    # -----------------------------------------------------
    # METHOD UPDATE MANY
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def update_many(self, filter_query: dict, new_values: dict):
        return self.entities.update_many(filter_query, {"$set": new_values})

    # -----------------------------------------------------
    # METHOD CREATE
    # -----------------------------------------------------
    def create(self, values: dict):
        return self.entities.insert_one(values).inserted_id

    # -----------------------------------------------------
    # METHOD GET INDEX FIELDS
    # -----------------------------------------------------
    @abstractmethod
    def get_index_fields(self) -> List[str]:
        pass
