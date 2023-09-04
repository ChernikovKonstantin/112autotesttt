import allure
from assertpy import soft_assertions, assert_that
from selene import be
from selene.support.shared.jquery_style import s

from data.titles import Titles
from pages.common.base_element import BaseElement


class AccidentsAddressRepeatedDialog(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._title = self.element.s(f'//h2[text()="{Titles.TWO_HUNDRED_RADIUS}"]')
        self._content_search_block = self.element.s('//*[contains (@class, "content__search")]')
        self._bind_incident_btn = lambda incident_number: s(
            f'//td[contains(., "{incident_number}")]/..//button[contains (., "привязать")]')
        self._close_and_continue_filling_btn = self.element.s(
            './/button[contains (., "закрыть и продолжить заполнение новой")]')
        self._expands_details_btn = self.element.ss('//td[contains (@class, "focus-element")]')
        self._chain_btn = self.element.ss('//td[contains (@class, "chain")]')
        self._bookmark_btn = self.element.ss('//td[contains (@class, "bookmark")]')
        self._special_btn = self.element.ss('//td[contains (@class, "special")]')
        self._timer_btn = self.element.ss('//td[contains (@class, "timer")]')

    @allure.step('Проверка всплывающего окна: В радиусе 200 метров от данного адреса '
                 'есть зарегистрированные ранее происшествия:')
    def assure_elements_is_visible(self):
        self._title.with_(timeout=5).should(be.visible)
        with soft_assertions():
            with allure.step('Проверка заголовка окна'):
                assert_that(self._title.matching(be.visible)).is_true()
            with allure.step('Проверка отсутствия расширенного поиска'):
                assert_that(self._content_search_block.matching(be.not_.visible)).is_true()
            with allure.step('Проверка видимости элемента раскрытия блока с подробной информацией'):
                assert_that(self._expands_details_btn[0].matching(be.visible)).is_true()
            with allure.step('Проверка кнопки Связь'):
                assert_that(self._chain_btn[0].matching(be.visible)).is_true()
            with allure.step('Проверка кнопки Закрепление'):
                assert_that(self._bookmark_btn[0].matching(be.visible)).is_true()
            with allure.step('Проверка кнопки ЧС'):
                assert_that(self._special_btn[0].matching(be.visible)).is_true()
            with allure.step('Проверка кнопки Напоминание/будильник'):
                assert_that(self._timer_btn[0].matching(be.visible)).is_true()

    @allure.step('Привязать инцидент')
    def bind_incident(self, incident_number: str):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self._bind_incident_btn(incident_number).with_(timeout=5).should(be.clickable).click()
        return NewAccidentCardPage()

    @allure.step('Нажать на кнопку закрыть и продолжить заполнение новой')
    def click_close_and_continue_filling_button(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self._close_and_continue_filling_btn.click()
        return NewAccidentCardPage()
