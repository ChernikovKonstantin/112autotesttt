import allure
from assertpy import soft_assertions, assert_that
from selene import query

from data.dates import get_current_date
from data.users.user_list import User
from pages.common.base_element import BaseElement


class IncidentContainer(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._title = self.element.s('.title')
        self._date = self.element.s('.date')
        self._operator = self.element.s('.operator')

    @allure.step('Проверка блока общей информации')
    def assure_incident_container(self, title: str, operator: User):
        with soft_assertions():
            assert_that(self._title.get(query.text)).is_equal_to(title)
            assert_that(self._date.get(query.text)).contains(f'Сохр. {get_current_date()} в ')
            assert_that(self._operator.get(query.text)).is_equal_to(f'Опер. , АРМ {operator.arm}, {operator.name}')
