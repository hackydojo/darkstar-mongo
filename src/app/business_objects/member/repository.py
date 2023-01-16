from typing import List
from app.business_objects.core_dao import EntityRepository


# =========================================================
# CLASS MEMBERS
# =========================================================
class Members(EntityRepository):

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


# =========================================================
# FUNCTION INJECT USERS
# =========================================================
def inject_vulnerabilities() -> Members:
    return Members()
