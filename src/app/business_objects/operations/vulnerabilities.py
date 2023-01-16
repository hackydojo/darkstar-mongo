from typing import List

from app.business_objects.repositories.vulnerability import Vulnerabilities
from app.models.vulnerability_operations import (
    VulnerabilityJiraIssueList,
    BulkTransitionResponseBasedOnJiraIDs,
    ControlDBStatusPerJiraIssue,
)
from app.types.core import IssueStatus


# =========================================================
# CLASS BULK TRANSITION VULNS BASED OIN JIRA IDS
# =========================================================
class BulkTransitionVulnerabilitiesBasedOnJiraIDs(object):
    def __init__(
        self,
        issues: VulnerabilityJiraIssueList,
        vulnerabilities: Vulnerabilities,
        target_status: IssueStatus = IssueStatus.MITIGATED_QUEUE,
    ):
        self.issues: VulnerabilityJiraIssueList = issues
        self.result: BulkTransitionResponseBasedOnJiraIDs = (
            BulkTransitionResponseBasedOnJiraIDs()
        )
        self.result.target_status = target_status.name
        self.vulnerabilities: Vulnerabilities = vulnerabilities
        self.target_status = target_status
        self.perform_transitions()

    # -----------------------------------------------------
    # PERFORM TRANSITIONS
    # -----------------------------------------------------
    def perform_transitions(self):
        for issue_id in self.issues.issues:
            if self.vulnerabilities.update_status_by_jira_id(
                issue_id, new_status=self.target_status
            ):
                self.result.found.append(issue_id)
            else:
                self.result.not_found.append(issue_id)

    # -----------------------------------------------------
    # PROPERTY OPERATION RESULT
    # -----------------------------------------------------
    @property
    def operation_result(self) -> BulkTransitionResponseBasedOnJiraIDs:
        return self.result


# =========================================================
# CLASS BULK STATUS GET BASED ON JIRA QUERY
# =========================================================


class GetStatusBasedOnMatchesFromJiraQuery(object):
    def __init__(
        self, issues: VulnerabilityJiraIssueList, vulnerabilities: Vulnerabilities
    ):
        self.issues: VulnerabilityJiraIssueList = issues
        self.vulnerabilities: Vulnerabilities = vulnerabilities
        self.found: List[ControlDBStatusPerJiraIssue] = []
        self.not_found: List[str] = []
        self.perform_query()

    # -----------------------------------------------------
    # PERFORM QUERY
    # -----------------------------------------------------
    def perform_query(self):
        for issue in self.issues.issues:
            vulnerability = self.vulnerabilities.get_by_jira_id(issue)
            if vulnerability:
                self.found.append(
                    ControlDBStatusPerJiraIssue(
                        issue_id=issue, cdb_status=vulnerability["status"]
                    )
                )
            else:
                self.not_found.append(issue)

    # -----------------------------------------------------
    # PROPERTY OPERATION RESULT
    # -----------------------------------------------------
    @property
    def operation_result(self):
        return {"found": self.found, "not_found": self.not_found}
