import allure
from assertpy import soft_assertions, assert_that
from selene import be
from selene.support.shared.jquery_style import s
from selenium.webdriver.common.keys import Keys

from data.titles import Titles
from pages.common.base_element import BaseElement


class NotifyAboutIncidentWindow(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 'v']
        self._title = self.element.s(f'//h1[text() = "{Titles.IS_ALARM_SURE}"]')
        self._yes_btn = self.element.s('.//button[normalize-space()="да"]')
        self._cancel_btn = self.element.s('.//button[normalize-space()="отмена"]')

    @allure.step('Проверка элементов модального оповещения специалиста')
    def assure_elements_is_visible(self):
        with soft_assertions():
            with allure.step('Проверка заголовка окна'):
                assert_that(self._title.matching(be.visible)).is_true()
            with allure.step('Проверка кнопок'):
                assert_that(self._yes_btn.matching(be.visible)).is_true()
                assert_that(self._cancel_btn.matching(be.visible)).is_true()

    @allure.step('Открытие окна создания напоминания при помощи клавиатуры')
    def open_window_by_keyword(self):
        s('//body').press(self._keyboard_combinations)
        return self

    @allure.step('Нажать на кнопку Отмена')
    def click_cancel_button(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self._cancel_btn.click()
        return NewAccidentCardPage()
