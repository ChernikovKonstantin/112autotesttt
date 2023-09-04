import random
from dataclasses import dataclass
from typing import Optional

from api.rest import RestApi
from data.builders.base_builder import BaseBuilder
from data.users.user_list import Users


@dataclass
class ApplicantNameFormData:
    name: Optional[str] = None
    status: Optional[str] = None
    channel: Optional[str] = None
    on_foreign_language: Optional[bool] = False


class ApplicantNameBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self._name: Optional[str] = None
        self._status: Optional[str] = None
        self._channel: Optional[str] = None
        self._on_foreign_language: Optional[bool] = False

    def with_name(self, name: str):
        self._name = name
        return self

    def with_status(self, status: str):
        self._status = status
        return self

    def with_channel(self, channel: str):
        self._channel = channel
        return self

    def with_foreign_language(self):
        self._on_foreign_language = True
        return self

    def with_random_name(self):
        self._name = f'{self._faker.first_name()} {self._faker.last_name()}'
        return self

    def with_random_status(self):
        self._status = random.choice(RestApi(user=Users.SPECIALIST_1).get_reporter_statuses())
        return self

    def random(self):
        self.with_random_name()
        self.with_random_status()
        return self

    def build(self):
        return ApplicantNameFormData(
            name=self._name,
            status=self._status,
            channel=self._channel,
            on_foreign_language=self._on_foreign_language,
        )
