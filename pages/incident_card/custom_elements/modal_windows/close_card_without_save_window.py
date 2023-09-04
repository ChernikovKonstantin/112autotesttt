import allure
from assertpy import soft_assertions, assert_that
from selene import be
from selene.support.shared.jquery_style import s
from selenium.webdriver.common.keys import Keys

from data.buttons import Buttons
from data.titles import Titles
from pages.common.base_element import BaseElement


class CloseCardWithoutSaveWindow(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ESCAPE]
        self._title = self.element.s(f'//h1[text() = "{Titles.IS_CLOSE_CARD_WITHOUT_SAFE}"]')
        self._save_and_close_btn = self.element.s(f'.//button[contains (text(), "{Buttons.SAVE_AND_CLOSE_CARD}")]')
        self._card_not_needed_confirm_btn = self.element.s(f'.//button[contains (text(), "{Buttons.CARD_NOT_NEEDED}")]')
        self._return_to_fill_card_btn = self.element.s(f'.//button[contains (text(), "{Buttons.RETURN_TO_FILL_CARD}")]')

    @allure.step('Проверка элементов модального окна: "Список оповещаемых служб"')
    def assure_elements_is_visible(self):
        with soft_assertions():
            with allure.step('Проверка заголовка окна'):
                assert_that(self._title.matching(be.visible)).is_true()
            with allure.step('Проверка кнопок'):
                assert_that(self._return_to_fill_card_btn.matching(be.visible)).is_true()
                assert_that(self._save_and_close_btn.matching(be.visible)).is_true()
                assert_that(self._card_not_needed_confirm_btn.matching(be.visible)).is_true()

    @allure.step('Открытие окна закрытия карточки без сохранения')
    def open_window_by_keyword(self):
        s('//body').press(self._keyboard_combinations)
        return self

    @allure.step('Нажать на кнопку Вернуться к заполнению')
    def click_return_to_fill_button(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self._return_to_fill_card_btn.click()
        return NewAccidentCardPage()
