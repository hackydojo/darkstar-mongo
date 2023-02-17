from typing import List
from app.business_objects.core.dao import EntityRepository
from app.business_objects.core.dao import inject_mongodb_error_handling


# =========================================================
# CLASS USERS
# =========================================================
class Users(EntityRepository):
    """
    Data Access Object that abstracts interactions with the
    database and at the same time, abstracts the specific
    database implementation.
    """

    # -----------------------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------------------
    def __init__(self):
        super().__init__(collection_name="users")

    # -----------------------------------------------------
    # GET INDEX FIELDS
    # -----------------------------------------------------
    def get_index_fields(self) -> List[str]:
        return ["id", "email"]

    # -----------------------------------------------------
    # GET BY USERNAME
    # -----------------------------------------------------
    @inject_mongodb_error_handling
    def get_by_username(self, username: str) -> dict or None:
        """
        Gets a user by its username if it exists. Otherwise,
        it throws an exception
        :param username: The username of the user
        :return: dict or None
        """
        return self.get({"username": username}).pop()
