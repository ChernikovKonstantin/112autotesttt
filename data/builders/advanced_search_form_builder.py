from dataclasses import dataclass
from typing import Optional

from data.builders.base_builder import BaseBuilder


@dataclass
class AdvancedSearchFormData:
    user_arm: Optional[str] = None
    status: Optional[str] = None
    incident_id: Optional[str] = None
    group_name: Optional[str] = None


class AdvancedSearchFormBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self._user_arm: Optional[str] = None
        self._status: Optional[str] = None
        self._incident_id: Optional[str] = None
        self._group_name: Optional[str] = None

    def with_user_arm(self, user_arm: str):
        self._user_arm = user_arm
        return self

    def with_status(self, status: str):
        self._status = status
        return self

    def with_incident_id(self, incident_id: str):
        self._incident_id = incident_id
        return self

    def with_group_name(self, group_name: str):
        self._group_name = group_name
        return self

    def build(self):
        return AdvancedSearchFormData(
            user_arm=self._user_arm,
            status=self._status,
            incident_id=self._incident_id,
            group_name=self._group_name,
        )
