import allure
from assertpy import assert_that
from selene import be

from api.rest import RestApi
from data.buttons import Buttons
from data.errors import MESSAGE_NO_MORE_THAN_18
from data.titles import Titles
from data.checkboxes import Checkboxes
from data.users.user_list import Users
from pages.common.base_element import BaseElement
from selene_custom import query


class CreateSmsDialog(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._title = self.element.s(f'//h2[text() = "{Titles.SEND_SMS_MESSAGE}"]')
        self._text_error = self.element.s(f'//p[text()="{MESSAGE_NO_MORE_THAN_18}"]')
        self._message_templates = self.element.ss('//button[contains (@class, "message-templates")]')
        self._all_phone_checkbox = self.element.s(f'//md-checkbox/*[contains (text(), "{Checkboxes.ON_ALL_NUMBERS}")]')
        self._textarea_create_sms = self.element.s('//textarea[contains (@class, "create-sms-modal")]')
        self._send_button = self.element.s(
            f'//button[@class="button-transparent blue" and contains (text(), "{Buttons.SEND}")]')
        self._close_button = self.element.s(
            f'//button[@class="button-transparent blue" and contains (text(), "{Buttons.CLOSE}")]')

    @allure.step('Проверка всплывающего окна: Отправка СМС-сообщения заявителю.')
    def assure_dialog_container(self):
        with allure.step('Проверка заголовка окна'):
            assert_that(self._title.matching(be.visible)).is_true()
        with allure.step('Проверка сообщения о кол-ве слов в тексте'):
            assert_that(self._text_error.matching(be.visible)).is_true()
        with allure.step('Проверка шаблонов сообщений'):
            message_templates_ui = [template.get(query.text) for template in self._message_templates]
            templates = RestApi(user=Users.SPECIALIST_1).get_message_templates()
            for template in templates:
                assert_that(message_templates_ui).contains(template)
        with allure.step('Проверка чекбокса'):
            assert_that(self._all_phone_checkbox.matching(be.visible)).is_true()
        with allure.step('Проверка плейсхолдера'):
            assert_that(self._textarea_create_sms.get(query.placeholder_value)).contains('введите текст сообщения')
        with allure.step('Проверка кнопок'):
            assert_that(self._send_button.matching(be.visible)).is_true()
            assert_that(self._close_button.matching(be.visible)).is_true()

    @allure.step('Отправка сообщения')
    def send_message(self, text: str):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self._textarea_create_sms.set_value(text)
        self._send_button.click()
        return NewAccidentCardPage()
