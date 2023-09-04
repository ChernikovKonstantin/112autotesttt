from typing import List

import allure
from assertpy import assert_that
from selene import be

from pages.common.base_element import BaseElement
from pages.custom_elements import AppDropdown
from utils.service_utils import wait_seconds


class ChangeStatusModalWindow(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._status = AppDropdown(xpath='//label[.="Статус"]/following-sibling::md-select')
        self._save_and_close_btn = self.element.s('//button[contains (., "сохранить и закрыть")]')

    @allure.step('Проверка отображения статусов')
    def assure_allowed_statuses(self, *statuses: [List[str], str]):
        wait_seconds(0.3)  # старые статусы не успевают удаляться из дропдауна
        status_options = self._status.click().get_options()
        for status in statuses:
            assert_that(status_options).contains(status)
        assert_that(len(status_options)).is_equal_to(len(statuses))

    @allure.step('Выбор статуса службы')
    def choose_status(self, status: str):
        self._status.choose_value(value=status)
        return self

    @allure.step('Сохранить и закрыть модальное окно')
    def save_and_close(self):
        from pages.search_main_page.search_page import SearchPage
        self._save_and_close_btn.should(be.clickable, timeout=5).click()
        return SearchPage()
