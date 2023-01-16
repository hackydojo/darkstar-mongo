from abc import abstractmethod, ABCMeta
from typing import List, Dict

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
from app.types.core import IssueStatus
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
            print(f"Error ID: 1")
            logging.error("Unable to find document")
            logging.error(str(ie))
        except NetworkTimeout as nt:
            print(f"Error ID: 2")
            logging.error(str(nt))
        except AutoReconnect as ar:
            print(f"Error ID: 3")
            logging.error(str(ar))
        except BulkWriteError as bwe:
            print(f"Error ID: 4")
            if bwe.timeout:
                logging.error(str(bwe))
            logging.error(str(bwe))
        except CollectionInvalid as collection_invalid_error:
            print(f"Error ID: 5")
            logging.error(str(collection_invalid_error))
        except InvalidURI as invalid_url_error:
            print(f"Error ID: 6")
            logging.error(str(invalid_url_error))
        except ConfigurationError as configuration_error:
            print(f"Error ID: 7")
            logging.error(str(configuration_error))
        except ConnectionFailure as connection_failure_error:
            print(f"Error ID: 8")
            logging.error(str(connection_failure_error))
        except CursorNotFound as cursor_not_found_error:
            print(f"Error ID: 9")
            logging.error(str(cursor_not_found_error))
        except DocumentTooLarge as document_too_large_error:
            print(f"Error ID: 10")
            logging.error(str(document_too_large_error))
        except DuplicateKeyError as duplicated_key_error:
            print(f"Error ID: 11")
            logging.error(str(duplicated_key_error))
        except EncryptionError as ece:
            print(f"Error ID: 12")
            logging.error(str(ece.cause))
        except ExecutionTimeout as timeout_error:
            print(f"Error ID: 13")
            logging.error(str(timeout_error))
        except InvalidName as invalid_name_error:
            print(f"Error ID: 14")
            logging.error(str(invalid_name_error))
        except InvalidOperation as invalid_operation_error:
            print(f"Error ID: 15")
            logging.error(str(invalid_operation_error))
        except PyMongoError as pymongo_error:
            print(f"Error ID: 16")
            logging.error(str(pymongo_error))
        except WriteError as write_error:
            print(f"Error ID: 17")
            logging.error(str(write_error))
        except WriteConcernError as write_concern_error:
            print(f"Error ID: 18")
            logging.error(str(write_concern_error))
        except Exception as error:
            print(f"Error ID: 19 {error}")
            logging.error(str(error))
        return False

    return error_handling_wrapper


# =========================================================
# CLASS HEIMDALL ENTITY REPOSITORY
# =========================================================
class EntityRepository(object):
    __metaclass__ = ABCMeta

    def __init__(self, collection_name: str, context: ServerContext = get_context()):
        """
        VAPControlDBService is not designed to be instantiated
        directly because it is an abstract class. This class
        provides a set of generic _operations on top of VAPs
        ControlDB. Specific actions should be implemented in
        classes that extend this class.

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
    # METHOD GET BY JIRA ID
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def get_by_jira_id(self, jira_id: str) -> Dict or None:
        """
        Finds an entity with a Matching Jira identifier
        :param jira_id:
        :return:
        """
        return self.get({"jira_id": jira_id}).pop()

    # -----------------------------------------------------
    # METHOD GET BY JIRA ID
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def get_by_status(self, statuses: List[IssueStatus], query: dict = None):
        if not query:
            query = {}
        query["$and"] = []
        for status in statuses:
            query["$and"].append({"status": str(status)})
        return self.get(query=query)

    # -----------------------------------------------------
    # METHOD GET WITHOUT STATUS
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def get_without_status(
        self, excluded_statuses: List[IssueStatus], query: dict = None
    ):
        if not query:
            query = {}
        query["$and"] = []
        for status in excluded_statuses:
            query["$and"].append({"status": {"$ne": str(status)}})
        return self.get(query=query)

    # -----------------------------------------------------
    # METHOD UPDATE ONE
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def update_one(self, issue_id: str, new_values: dict):
        return self.entities.update_one({"id": issue_id}, {"$set": new_values})

    # -----------------------------------------------------
    # METHOD UPDATE ONE BY JIRA ID
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def update_one_by_jira_id(self, jira_id: str, new_values: dict):
        return self.entities.update_one({"jira_id": jira_id}, {"$set": new_values})

    # -----------------------------------------------------
    # METHOD UPDATE MANY
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def update_many(self, filter_query: dict, new_values: dict):
        return self.entities.update_many(filter_query, {"$set": new_values})

    # -----------------------------------------------------
    # METHOD UPDATE STATUS FOR ONE
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def update_status_for_one(self, issue_id: str, new_status: IssueStatus):
        return self.update_one(
            issue_id=issue_id, new_values={"status": str(new_status)}
        )

    # -----------------------------------------------------
    # METHOD UPDATE STATUS BY JIRA ID
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def update_status_by_jira_id(self, jira_id: str, new_status: IssueStatus):
        return self.update_one_by_jira_id(
            jira_id=jira_id, new_values={"status": str(new_status)}
        )

    # -----------------------------------------------------
    # METHOD UPDATE STATUS FOR MANY
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def update_status_for_many(self, filter_query: dict, new_status: IssueStatus):
        return self.update_many(
            filter_query=filter_query, new_values={"status": str(new_status)}
        )

    # -----------------------------------------------------
    # METHOD GET INDEX FIELDS
    # -----------------------------------------------------
    @abstractmethod
    def get_index_fields(self) -> List[str]:
        pass
