from dataclasses import dataclass
from typing import Optional

from data.builders.base_builder import BaseBuilder


@dataclass
class RecordCallFormData:
    date: Optional[str] = None
    status: Optional[str] = None
    phone_number: Optional[str] = None
    text: Optional[str] = None
    empty_list: Optional[bool] = False


class RecordCallBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self._date: Optional[str] = None
        self._status: Optional[str] = None
        self._phone_number: Optional[str] = None
        self._message_text: Optional[str] = None
        self._empty_list: Optional[bool] = False

    def with_date(self, date: str):
        self._date = date
        return self

    def with_status(self, status: str):
        self._status = status
        return self

    def with_phone_number(self, phone_number: str):
        self._phone_number = phone_number
        return self

    def with_message_text(self, message_text: str):
        self._message_text = message_text
        return self

    def with_empty_list(self):
        self._empty_list = True
        return self

    def build(self):
        return RecordCallFormData(
            date=self._date,
            status=self._status,
            phone_number=self._phone_number,
            text=self._message_text,
            empty_list=self._empty_list,
        )
