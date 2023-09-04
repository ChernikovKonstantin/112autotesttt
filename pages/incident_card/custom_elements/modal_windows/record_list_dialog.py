import allure
from assertpy import assert_that, soft_assertions
from selene import be, command
from selene.support.shared.jquery_style import s

from data.builders.record_call_builder import RecordCallFormData
from data.buttons import Buttons
from data.titles import Titles
from pages.common.base_element import BaseElement


class RecordListDialog(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._title = self.element.s(f'//h2[text()="{Titles.CALL_RECORDS}"]')
        self._return_to_card_button = self.element.s(f'//button//*[contains (text(), "{Buttons.RETURN_TO_CARD}")]')
        self._empty_list = self.element.s(f'//h1[contains (text(), "{Titles.NO_RECORDS_FOUND}")]')

    def assure_dialog_container(self, form_data: RecordCallFormData):
        with soft_assertions():
            with allure.step('Проверка заголовка окна'):
                assert_that(self._title.matching(be.visible)).is_true()
            with allure.step('Проверка отсутствия записей'):
                if form_data.empty_list:
                    assert_that(self._empty_list.matching(be.visible)).is_true()
            with allure.step('Проверка кнопки Вернуться в карточку'):
                assert_that(self._return_to_card_button.matching(be.enabled)).is_true()

    @allure.step('Нажать на кнопку Вернуться в карточку')
    def click_return_to_card_button(self):
        self._return_to_card_button.perform(command.js.click)

    @allure.step('Закрыть страницу при помощи клавиатуры')
    def close_page_by_keyboard(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        s('//body').press_escape()
        return NewAccidentCardPage()
