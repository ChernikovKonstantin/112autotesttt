from typing import List

import allure
from assertpy import soft_assertions, assert_that
from selene import be, query
from selene.support.shared.jquery_style import s
from selenium.webdriver.common.keys import Keys

from data.buttons import Buttons
from data.titles import Titles
from pages.common.base_element import BaseElement


class SaveIncidentWindow(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 's']
        self._title = self.element.s(f'//h1[text() = "{Titles.SERVICES_LIST}"]')
        self._notify_and_save_btn = self.element.s(f'.//button[contains (., "{Buttons.NOTIFY_AND_SAVE_CARD}")]')
        self._return_to_fill_btn = self.element.s(f'.//button[contains (., "{Buttons.RETURN_TO_FILL}")]')
        self._services_titles = self.element.ss('//*[@class= "service-title-container"]')
        self._need_call = lambda service: self.element.s(f'//*[@class="service-title-container"'
                                                         f' and contains(., "{service}")]'
                                                         '/parent::*/p[//p[contains (., "нужен")'
                                                         ' and contains (., "звонок")]]')

    @allure.step('Проверка элементов модального окна: "Список оповещаемых служб"')
    def assure_elements_is_visible(self):
        with soft_assertions():
            with allure.step('Проверка заголовка окна'):
                assert_that(self._title.matching(be.visible)).is_true()
            with allure.step('Проверка кнопок'):
                assert_that(self._notify_and_save_btn.matching(be.visible)).is_true()
                assert_that(self._return_to_fill_btn.matching(be.visible)).is_true()

    @allure.step('Проверка отображения служб для оповещения')
    def assure_services(self, services: List):
        with allure.step('Проверка служб для оповещения'):
            services_ui = [service.get(query.text) for service in self._services_titles]
            for service in services:
                assert_that(services_ui).contains(service['shortTitle'])

    @allure.step('Открытие окна сохранения карточки при помощи клавиатуры')
    def open_window_by_keyword(self):
        s('//body').press(self._keyboard_combinations)
        return self

    @allure.step('Нажать на кнопку Вернуться к заполнению')
    def click_return_to_fill_button(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self._return_to_fill_btn.click()
        return NewAccidentCardPage()

    @allure.step('Нажать на кнопку Оповестить и сохранить карточку')
    def click_notify_and_save_button(self):
        from pages.incident_card.saved_accident_сard_page import SavedAccidentCardPage
        self._notify_and_save_btn.click()
        return SavedAccidentCardPage()

    @allure.step('Проверка служб вне сети')
    def assure_offline_services(self, services):
        for service in services:
            if service['network'] == 0:
                assert_that(self._need_call(service['shortTitle']).matching(be.visible)).is_true()
