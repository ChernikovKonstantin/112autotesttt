from typing import List

import allure
from assertpy import assert_that, soft_assertions
from selene import be, command

from data.color_data import Color
from pages.common.base_element import BaseElement
from selene_custom import query
from utils.service_utils import get_background_color


class AddServiceModalWindow(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._input = self.element.s('.//input')
        self._service_item = lambda item: self.element.s(f'//li[contains (text(), "{item}")]')
        self._service_item_full = lambda item: self.element.s(f'//li//*[contains (text(), "{item}")]')
        self._save_and_close_btn = self.element.s('//button[contains (text(), "Сохранить и закрыть")]')

        self.element.with_(timeout=5).should(be.visible)

    @allure.step("Добавить службы")
    def added_services(self, services: List):
        for service in services:
            self._input.set_value(service['shortTitle'])
            service_item = self._service_item_full(service['fullTitle']) if service['fullTitle'] \
                else self._service_item(service['shortTitle'])
            service_item.should(be.clickable, timeout=5).click()
        self._input.clear()
        return self

    @allure.step("Проверить свойства добавленных служб в модальном окне")
    def assure_added_services(self, services: List):
        with soft_assertions():
            for service in services:
                service_item = self._service_item_full(service['fullTitle']).element('..') if service['fullTitle'] \
                    else self._service_item(service['shortTitle'])
                service_item.perform(command.js.scroll_into_view)
                with allure.step(f"Проверка: элемент со службой {service} содержит класс active"):
                    assert_that(service_item.get(query.class_value)).contains('active')
                with allure.step(f"Проверка: элемент со службой {service} подсвечивается синим"):
                    assert_that(get_background_color(service_item)).is_equal_to(Color.BLUE)
        return self

    @allure.step("Нажать кнопку 'Сохранить и закрыть' в модальном окне")
    def save_and_close_button_click(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self._save_and_close_btn.click()
        return NewAccidentCardPage()
