from dataclasses import dataclass
from typing import Optional

from data.builders.base_builder import BaseBuilder
from utils.service_utils import get_text_with_max_nb_chars


@dataclass
class SmsHistoryFormData:
    date: Optional[str] = None
    status: Optional[str] = None
    phone_number: Optional[str] = None
    text: Optional[str] = None


class SmsHistoryBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self._date: Optional[str] = None
        self._status: Optional[str] = None
        self._phone_number: Optional[str] = None
        self._message_text: Optional[str] = None

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

    def with_random_message_text(self):
        self._message_text = get_text_with_max_nb_chars(max_nb_chars=18)
        return self

    def random(self):
        self.with_random_message_text()
        return self

    def build(self):
        return SmsHistoryFormData(
            date=self._date,
            status=self._status,
            phone_number=self._phone_number,
            text=self._message_text,
        )
