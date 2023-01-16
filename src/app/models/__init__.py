from pydantic import BaseModel, Field
from typing import List, Dict, Optional


# =========================================================
# CLASS SECURITY CENTER REPOSITORY
# =========================================================
class SecurityCenterRepository(BaseModel):
    business_unit: Optional[str]
    c_code: Optional[str]
    env: Optional[str]
    name: Optional[str]
    repository_id: Optional[str]
    type: Optional[str]


# =========================================================
# CLASS HEIMDALL MODEL
# =========================================================
class HeimdallModel(BaseModel):

    id: str = Field(None, title="Unique identifier")

    datacenter: Optional[str]
    repository: Optional[SecurityCenterRepository]
    asset_group: Optional[str]
    jira_id: Optional[str]
    ownership: Optional[str]
    status: Optional[str]
    priority: Optional[str]
    last_seen: Optional[str]
    solution: Optional[str]
    plugin_output: Optional[str or Dict]
    plugin_info: Optional[str or Dict]
    plugin_name: Optional[str or Dict]
    plugin_id: Optional[str]
    description: Optional[str]
    dns_name: Optional[str]
    protocol: Optional[str]
    port: Optional[str]
    ip: Optional[str]
    severity: Optional[str]

    @property
    def model_fields(self) -> List[str]:
        return [
            "id",
            "datacenter",
            "repository",
            "asset_group",
            "jira_id",
            "ownership",
            "status",
            "priority",
            "last_seen",
            "solution",
            "plugin_output",
            "plugin_info",
            "plugin_name",
            "plugin_id",
            "description",
            "dns_name",
            "protocol",
            "port",
            "ip",
            "severity",
        ]


# =========================================================
# CLASS HEIMDALL MODEL
# =========================================================
class Vulnerability(HeimdallModel):

    cve: Optional[List[str or Dict]]
    exploit_available: Optional[str]
    exploit_frameworks: Optional[str]
    see_also: Optional[str]

    @property
    def model_fields(self) -> List[str]:
        base_fields = super().model_fields
        base_fields.append("cve")
        base_fields.append("exploit_available")
        base_fields.append("exploit_frameworks")
        base_fields.append("see_also")
        return base_fields


# =========================================================
# CLASS HEIMDALL MODEL
# =========================================================
class Benchmark(HeimdallModel):
    pass
