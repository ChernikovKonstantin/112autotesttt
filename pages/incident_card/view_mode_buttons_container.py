import allure
from assertpy import soft_assertions, assert_that
from selene import be
from selenium.webdriver.common.keys import Keys

from data.color_data import Color
from pages.common.base_element import BaseElement
from selene_custom import query
from utils.service_utils import get_background_color


class ViewModeButtonsContainer(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._view_btn = self.element.s('//button[normalize-space()="просмотр"]')
        self._addition_btn = self.element.s('//button[normalize-space()="дополнение"]')

    @allure.step("Проверка кнопок")
    def assure_buttons(self):
        with soft_assertions():
            with allure.step('Проверка кнопки Просмотр'):
                assert_that(self._view_btn.with_(timeout=10).get(query.class_value)).contains('active')
                assert_that(get_background_color(self._view_btn)).is_equal_to(Color.BLUE)
            with allure.step('Проверка кнопки Дополнение'):
                assert_that(self._addition_btn.matching(be.visible)).is_true()
        return self

    @allure.step("Активация режима дополнения")
    def activate_additional_mode(self):
        from pages.incident_card.additional_mode_card_page import AdditionalModeCardPage
        self._addition_btn.press(Keys.SHIFT, Keys.F2)
        return AdditionalModeCardPage()
