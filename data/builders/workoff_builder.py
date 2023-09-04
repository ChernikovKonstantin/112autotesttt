from dataclasses import dataclass
from typing import Optional

from data.builders.base_builder import BaseBuilder
from utils.service_utils import get_text_with_max_nb_chars


@dataclass
class WorkoffFormData:
    operator_id: Optional[str] = None
    operator_arm: Optional[str] = None
    start_date_time: Optional[str] = None
    save_workoff_time: Optional[str] = None
    service: Optional[str] = None
    call_destination: Optional[str] = None
    phone_humber: Optional[str] = None
    username: Optional[str] = None
    description: Optional[str] = None


class WorkoffFormBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self._operator_id: Optional[str] = None
        self._operator_arm: Optional[str] = None
        self._start_date_time: Optional[str] = None
        self._save_workoff_time: Optional[str] = None
        self._service: Optional[str] = None
        self._call_destination: Optional[str] = None
        self._phone_humber: Optional[str] = None
        self._username: Optional[str] = None
        self._description: Optional[str] = None

    def with_operator_id(self, operator_id: str):
        self._operator_id = operator_id
        return self

    def with_operator_arm(self, operator_arm: str):
        self._operator_arm = operator_arm
        return self

    def with_start_date_time(self, start_date_time: str):
        self._start_date_time = start_date_time
        return self

    def with_save_workoff_time(self, save_workoff_time: str):
        self._save_workoff_time = save_workoff_time
        return self

    def with_service(self, service: str):
        self._service = service
        return self

    def with_call_destination(self, call_destination: str):
        self._call_destination = call_destination
        return self

    def with_phone_number(self, phone_humber: str):
        self._phone_humber = phone_humber
        return self

    def with_username(self, username: str):
        self._username = username
        return self

    def with_description(self, description: str):
        self._description = description
        return self

    def with_random_name(self):
        self._username = f'{self._faker.first_name()} {self._faker.last_name()}'
        return self

    def with_random_description(self):
        self._description = get_text_with_max_nb_chars(max_nb_chars=200).replace('\n', '')
        return self

    def with_random_call_destination(self):
        self._call_destination = get_text_with_max_nb_chars(max_nb_chars=25).replace('\n', '')
        return self

    def random(self):
        self.with_random_name()
        self.with_random_description()
        self.with_random_call_destination()
        return self

    def build(self):
        return WorkoffFormData(
            operator_id=self._operator_id,
            operator_arm=self._operator_arm,
            start_date_time=self._start_date_time,
            save_workoff_time=self._save_workoff_time,
            service=self._service,
            call_destination=self._call_destination,
            phone_humber=self._phone_humber,
            username=self._username,
            description=self._description,
        )
