import allure
from assertpy import assert_that, soft_assertions
from selene import be

from data.builders.sms_history_builder import SmsHistoryFormData
from data.buttons import Buttons
from data.table_columns import SMS_HISTORY
from data.titles import Titles
from pages.common.base_element import BaseElement
from selene_custom import query
from utils.service_utils import clean_phone_number


class SmsHistoryDialog(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._title = self.element.s(f'//h2[text()="{Titles.SMS_MESSAGE_HISTORY}"]')
        self._table_header_columns = self.element.ss('//th[contains (@class, "sms-history-call-head")]')
        self._sms_history_date = self.element.s('//td[contains (@class, "sms-history-date")]')
        self._sms_history_status = self.element.s('//td[contains (@class, "sms-history-status")]')
        self._sms_history_phone = self.element.s('//td[contains (@class, "sms-history-phone")]')
        self._sms_history_text = self.element.s('//td[contains (@class, "sms-history-text")]')
        self._return_to_card_button = self.element.s(f'//button//*[text()= "{Buttons.RETURN_TO_CARD}"]')

        self.element.with_(timeout=5).should(be.visible)

    @allure.step('Проверка всплывающего окна: История сообщений.')
    def assure_dialog_container(self, form_data: SmsHistoryFormData):
        with soft_assertions():
            with allure.step('Проверка заголовка окна'):
                assert_that(self._title.matching(be.visible)).is_true()
            with allure.step('Проверка заголовков таблицы'):
                table_headers_column_ui = [column.get(query.text) for column in self._table_header_columns]
                for column in SMS_HISTORY:
                    assert_that(table_headers_column_ui).contains(column)
            with allure.step('Проверка текста сообщения'):
                if form_data.date:
                    assert_that(self._sms_history_date.get(query.text)).contains(form_data.date)
                if form_data.status:
                    assert_that(self._sms_history_status.get(query.text)).contains(form_data.status)
                if form_data.phone_number:
                    assert_that(clean_phone_number(self._sms_history_phone.get(query.text))).contains(
                        form_data.phone_number)
                if form_data.text:
                    assert_that(self._sms_history_text.get(query.text)).contains(form_data.text)
            with allure.step('Проверка кнопки Вернуться в карточку'):
                assert_that(self._return_to_card_button.matching(be.visible)).is_true()

    @allure.step('Нажать на кнопку Вернуться в карточку')
    def click_return_to_card_button(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self._return_to_card_button.click()
        return NewAccidentCardPage()
