import allure
from assertpy import assert_that
from selene import be
from selenium.webdriver.common.keys import Keys

from data.color_data import Color
from pages.incident_card.base_container import BaseContainer
from utils.service_utils import clean_phone_number

from selene.api import have, query


class BasePhoneContainer(BaseContainer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._input = self.element.s('.//input')
        self._foreign_number_button = self.element.s('.//button[@title="Зарубежный номер"]')
        self._sms_button = self.element.s('//button[@title="Отправить SMS"]')
        self._call_button = self.element.s('//button[@title="Вызов"]')
        self._keyboard_combinations = []

    @allure.step('Заполнение номера телефона')
    def fill_phone(self, number: str):
        self._input.type(text=number)

    @allure.step('Клик по кнопке Зарубежный номер')
    def click_foreign_button(self):
        self._foreign_number_button.click()

    @allure.step('Клик по кнопке Отправить смс')
    def click_send_sms_button(self):
        from pages.incident_card.custom_elements.modal_windows.create_sms_window import CreateSmsDialog
        self._sms_button.click()
        return CreateSmsDialog(css='#createSmsDialog')

    @allure.step('Проверка телефона')
    def assure_phone(self, number: str):
        assert_that(clean_phone_number(self._input.get(query.value))).contains(number)

    @allure.step('Проверка: блок активный')
    def is_active(self):
        self.element.with_(timeout=10).should(have.css_class('highlight-active'))


class AonPhoneContainer(BasePhoneContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, Keys.F1]
        self._get_location_button = self.element.s('//button[@title="Получить местоположение"]')
        self._get_user_data_button = self.element.s('//button[@title="Получить данные абонента"]')
        self._elements_for_assert = [self._call_button,
                                     self._sms_button,
                                     self._foreign_number_button,
                                     self._get_location_button,
                                     self._get_user_data_button,
                                     ]

    @allure.step('Клик по кнопке Получить местоположение')
    def click_get_location_button(self):
        self._get_location_button.click().with_(timeout=5).should(have.css_property('color', Color.RGBA_GREEN))
        return self


class OthersPhoneContainers(BasePhoneContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._copy_aon_button = self.element.s('//button[@title="Скопировать АОН"]')
        self._elements_for_assert = [self._call_button,
                                     self._sms_button,
                                     self._foreign_number_button,
                                     self._copy_aon_button,
                                     ]

    @allure.step('Клик по кнопке скопировать АОН')
    def copy_aon_button_click(self):
        self._copy_aon_button.click()


class ProvidedContainer(OthersPhoneContainers):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, Keys.F2]


class LocationContainer(OthersPhoneContainers):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, Keys.F3]
