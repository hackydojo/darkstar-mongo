from typing import List
from app.business_objects.core.dao import EntityRepository


# =========================================================
# CLASS MEMBERS
# =========================================================
class Members(EntityRepository):
    # -----------------------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------------------
    def __init__(self):
        super().__init__(collection_name="members")

    # -----------------------------------------------------
    # GET INDEX FIELDS
    # -----------------------------------------------------
    def get_index_fields(self) -> List[str]:
        return ["id", "email"]
