from typing import List

import allure
from assertpy import assert_that, soft_assertions
from selene import be
from selenium.webdriver.common.keys import Keys

from data.builders.applicant_name_builder import ApplicantNameFormData
from selene.api import query

from pages.incident_card.base_container import BaseContainer

from pages.custom_elements import AppDropdown, AppCheckbox


class ApplicantNameContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 'q']
        self._name = self.element.s('//*[@placeholder="Фамилия и имя заявителя"]')
        self._translate_button = AppCheckbox(xpath='//button[@title="Вызов на иностранном языке"]')
        self._user_status = AppDropdown(xpath='//md-select[@aria-label="выберите статус"]')
        self._incoming_channel = AppDropdown(xpath='//md-select[@aria-label="канал связи"]')

    @allure.step('Заполнение блока')
    def fill_block(self, form_data: ApplicantNameFormData):
        if form_data.name:
            self._name.should(be.clickable).click().set_value(form_data.name)
        if form_data.status:
            self._user_status.choose_value(form_data.status)
        if form_data.channel:
            self._incoming_channel.set_value_with_search_field(form_data.channel)
        if form_data.on_foreign_language:
            self._translate_button.set_value(status=True)

    @allure.step('Проверка заполнения блока')
    def assure_block(self, form_data: ApplicantNameFormData):
        with soft_assertions():
            if form_data.name:
                name = self._name.get(query.value) if self._name.get(query.value) else self._name.get(query.text)
                assert_that(name).contains(form_data.name)
            if form_data.status:
                assert_that(self._user_status.text).contains(form_data.status)
            if form_data.channel:
                assert_that(self._incoming_channel.text).contains(form_data.channel)
            if form_data.on_foreign_language:
                assert_that(self._translate_button.is_checked()).is_equal_to(form_data.on_foreign_language)

    @allure.step('Проверка статусов')
    def assure_statuses(self, statuses: List):
        self._user_status.click()
        ui_statuses = self._user_status.get_options()
        for item in statuses:
            assert_that(ui_statuses).contains(item)


class ApplicantNameContainerSaved(ApplicantNameContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name = self.element.s('//*[@class="name"]')
        self._translate_button = AppCheckbox(xpath='//button[@title="Вызов на иностранном языке"]')
        self._user_status = self.element.s('//*[@class="status"]')
        self._incoming_channel = self.element.s('//*[@class="channel"]')

