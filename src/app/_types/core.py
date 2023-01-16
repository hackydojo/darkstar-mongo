from enum import Enum


# =========================================================
# ENUM ISSUE STATUS
# =========================================================
class IssueStatus(Enum):
    PENDING_OWNERSHIP_LOOKUP = (0,)
    TICKETING = (1,)
    DISCOVERED = (2,)
    HOST_VULNERABLE = (3,)
    MITIGATED_QUEUE = (4,)
    HOST_NOT_PRESENT = (5,)
    RESOLVED = 6
    EXCLUDED_DELETED = (-1,)
    PLUGIN_ID_EXCLUDED = -2

    def __str__(self):
        return self.name
