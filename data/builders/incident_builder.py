from dataclasses import dataclass
from typing import Optional

from data.builders.base_builder import BaseBuilder


@dataclass
class IncidentFormData:
    address: Optional[dict] = None
    base_address: Optional[dict] = None
    user_arm: Optional[str] = None
    injured_count: Optional[str] = None
    gos_service_id: Optional[int] = None


class IncidentBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self._address: Optional[dict] = None
        self.base_address: Optional[dict] = None
        self._user_arm: Optional[str] = None
        self._injured_count: Optional[str] = None
        self._gos_service_id: Optional[int] = None

    def with_address(self, address: dict):
        self._address = address
        return self

    def with_base_address(self, address: dict):
        self._address = address
        return self

    def with_user_arm(self, user_arm: str):
        self._user_arm = user_arm
        return self

    def with_injured_count(self, injured_count: str):
        self._injured_count = injured_count
        return self

    def with_gos_service_id(self, gos_service_id: int):
        self._gos_service_id = gos_service_id
        return self

    def build(self):
        return IncidentFormData(
            address=self._address,
            user_arm=self._user_arm,
            injured_count=self._injured_count,
            gos_service_id=self._gos_service_id,
        )
