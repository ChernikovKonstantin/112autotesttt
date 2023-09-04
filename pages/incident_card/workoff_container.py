import allure
from assertpy import soft_assertions, assert_that
from selene import be, have, query

from data.builders.workoff_builder import WorkoffFormData
from data.color_data import Color
from data.dates import is_datetime_between_dates_with_delta
from pages.custom_elements import AppDropdown
from pages.incident_card.base_container import BaseContainer
from utils.service_utils import get_background_color

from selene.support.shared import browser
from selenium.webdriver import ActionChains


class WorkOffContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._operator_btn = self.element.s('//div[contains (@class, "operator")]//button')
        self._date = self.element.s('//div[contains (@class, "date")]')
        self._service = self.element.s('//div[contains (@class, "service")]')
        self._call_destination = self.element.s('//div[contains (@class, "call-destination")]//input')
        self._phone_humber = self.element.s('//div[contains (@class, "phone-humber")]')
        self._call_btn = self.element.s('//div[contains (@class, "call-icon")]/button')
        self._username = self.element.s('//div[contains (@class, "username")]//input')
        self._description = self.element.s('//div[contains (@class, "description")]//input')
        self._submit_btn = self.element.s('//div[contains (@class, "submit-button")]//button')
        self._add_workoff_service_dropdown = AppDropdown(xpath='//md-select[@placeholder="служба"]')
        self._tooltip = self.element.s('//md-tooltip')

        # строка с заполненным контентом по отработке
        self._last_row_with_content = self.element.s(f'//div[contains (@class, "content this-operator")][last()]')
        self._content_operator = self._last_row_with_content.s('./div[contains (@class, "operator")]')
        self._content_arm = self._last_row_with_content.s('./div[contains (@class, "arm")]')
        self._content_datetime = self._last_row_with_content.s('./div[contains (@class, "date")][1]')
        self._content_save_time = self._last_row_with_content.s('./div[contains (@class, "date")][2]')
        self._content_service = self._last_row_with_content.s('./div[contains (@class, "service")]')
        self._content_call_destination = self._last_row_with_content.s('./div[contains (@class, "call-destination")]')
        self._content_phone_number = self._last_row_with_content.s('./div[contains (@class, "phone-humber")]')
        self._content_call_btn = self._last_row_with_content.s('./div[contains (@class, "call-icon")]/button')
        self._content_username = self._last_row_with_content.s('./div[contains (@class, "username")]')
        self._content_description = self._last_row_with_content.s('./div[contains (@class, "description")]')

    @allure.step('Проверка видимости элементов')
    def assure_elements_is_visible(self):
        with soft_assertions():
            assert_that(self._operator_btn.matching(be.visible)).is_true()
            assert_that(self._date.matching(be.visible)).is_true()
            assert_that(self._service.matching(be.visible)).is_true()
            assert_that(self._call_destination.matching(be.visible)).is_true()
            assert_that(self._phone_humber.matching(be.visible)).is_true()
            assert_that(self._call_btn.matching(be.visible)).is_true()
            assert_that(self._username.matching(be.visible)).is_true()
            assert_that(self._description.matching(be.visible)).is_true()
            assert_that(self._submit_btn.matching(be.visible)).is_true()

    @allure.step('Открытие дропдауна Служба')
    def open_service_dropdown_by_keyboard(self):
        self._add_workoff_service_dropdown.element.press_enter()
        return self

    @allure.step('Выбор службы из дропдауна')
    def choose_service(self, service: str):
        self._add_workoff_service_dropdown.choose_value_from_open_dropdown(value=service)
        return self

    @allure.step('Заполнение формы отработки')
    def fill_form(self, service: str = None,
                  call_destination: str = None,
                  username: str = None,
                  description: str = None):
        if service:
            self._add_workoff_service_dropdown.choose_value(value=service)
        if call_destination:
            self._call_destination.set_value(value=call_destination)
        if username:
            self._username.set_value(value=username)
        if description:
            self._description.set_value(value=description)
        return self

    @allure.step('Сохранение формы отработки')
    def save_form(self):
        self._submit_btn.click().should(have.attribute('disabled', 'true'))
        return self

    @allure.step('Проверка формы отработки')
    def assure_last_row_form_data(self, form_data: WorkoffFormData):
        minutes_delta = 2
        with soft_assertions():
            if form_data.operator_id:
                assert_that(self._content_operator.get(query.text)).is_equal_to(str(form_data.operator_id))
            if form_data.start_date_time:
                date_time_from_ui = self._content_datetime.get(query.text).replace('\n', ' ')
                assert_that(is_datetime_between_dates_with_delta(date=date_time_from_ui, minutes_delta=minutes_delta),
                            f'Дата не попадает в диапазон minutes_delta={minutes_delta}').is_true()
            if form_data.save_workoff_time:
                time_from_ui = self._content_save_time.get(query.text)
                assert_that(is_datetime_between_dates_with_delta(date=time_from_ui, minutes_delta=minutes_delta),
                            f'Время не попадает в диапазон minutes_delta={minutes_delta}').is_true()
            if form_data.operator_arm:
                assert_that(self._content_arm.get(query.text)).is_equal_to(form_data.operator_arm)
            if form_data.service:
                assert_that(self._content_service.get(query.text)).is_equal_to(form_data.service)
            if form_data.call_destination:
                assert_that(self._content_call_destination.get(query.text)).is_equal_to(form_data.call_destination)
            if form_data.phone_humber:
                assert_that(self._content_phone_number.get(query.text)).is_equal_to(form_data.phone_humber)
            assert_that(self._content_call_btn.get(query.attribute('disabled'))).is_true()
            if form_data.username:
                assert_that(self._content_username.get(query.text)).is_equal_to(form_data.username)
            if form_data.description:
                assert_that(self._content_description.get(query.text)).is_equal_to(form_data.description)

    @allure.step('Проверка цвета у полей оператор, АРМ, дата и время начала создания отработки, время сохранения')
    def assure_last_row_color(self):
        for element in (self._content_operator, self._content_arm, self._content_datetime, self._content_save_time):
            assert_that(get_background_color(element)).is_equal_to(Color.CHERRY)

    @allure.step('Проверка тултипов у полей ФИО оператора, куда звонили, ФИО, суть сообщения')
    def assure_last_row_tooltips(self, operator: str, call_destination: str, username: str, description: str):
        with soft_assertions():
            for element, tooltip in [
                (self._content_operator, operator),
                (self._content_call_destination, call_destination),
                (self._content_username, username),
                (self._content_description, description),
            ]:
                ActionChains(browser.driver).move_to_element(element()).perform()
                assert_that(self._tooltip.should(be.visible, timeout=5).get(query.text)).contains(tooltip)
