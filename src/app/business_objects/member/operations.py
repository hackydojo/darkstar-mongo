from app.business_objects.core.ops import BusinessOperation
from app.business_objects.member import Members
from app.resources.members import MemberCreationRequest


# =========================================================
# CLASS CREATE MEMBER OPERATION
# =========================================================
class CreateMemberOperation(BusinessOperation):
    # -----------------------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------------------
    def __init__(self, member_request: MemberCreationRequest, members: Members):
        self.members = members
        self.member_request: MemberCreationRequest = member_request
        self.member_dict = self.member_request.dict()
        self.perform_transaction()

    # -----------------------------------------------------
    # PROPERTY OPERATION RESULT
    # -----------------------------------------------------
    @property
    def operation_result(self) -> any:
        return self.member_dict

    # -----------------------------------------------------
    # METHOD PERFORM TRANSACTION
    # -----------------------------------------------------
    def perform_transaction(self):
        mongo_id = self.members.create(self.member_request.dict(), self.members)
        self.member_dict["_id"] = str(mongo_id)
