import allure
from assertpy import soft_assertions, assert_that
from selene import be
from selenium.webdriver.common.keys import Keys

from data.builders.address_builder import AddressFormData
from data.color_data import Color

from selene.api import query

from data.errors import ADDRESS_NOT_FOUND
from pages.common.base_element import BaseElement
from pages.custom_elements.app_dropdown import DropDownSuggest, AppDropdown
from pages.incident_card.base_container import BaseContainer
from selene_custom import by
from utils.service_utils import get_text_color


class AddressContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 'a']
        self._address_dropdown = DropDownSuggest(xpath='//*[@aria-label="введите адрес"]')
        self._full_address = self.element.s('//input[@placeholder="введите адрес"]')
        self._address_field_input = lambda field: self.element.s(f'//label[text() ="{field}:"]').s(
            by.be_following_sibling('input'))
        self._dropdown_with_text = lambda text: AppDropdown(
            xpath=f'//md-select-label[.="{text}:"]/following-sibling::md-select')
        self._address_desc = self.element.s('//label[text() ="Описательный адрес:"]').s(
            by.be_following_sibling('*/textarea'))
        self._concurrence_btn = self.element.s('//*[contains (., "совпадение")]/self::button')
        self._clean_address_btn = self.element.s('//button[contains(., "очистить адрес")]')
        self._address_not_found_message = self.element.s(f'//span[.="{ADDRESS_NOT_FOUND}"]')

    @allure.step('Проверка списка с подсказками')
    def assure_suggestions(self, value: str, yandex_suggest_count: int, fias_suggest_count: int):
        self._address_dropdown.set_value(value)
        self._address_dropdown.scroll_to_end_suggest_list()
        ui_suggestions = ','.join(self._address_dropdown.get_last_suggestions())
        with soft_assertions():
            assert_that(ui_suggestions.count('Яндекс')).is_equal_to(yandex_suggest_count)
            assert_that(ui_suggestions.count('Организации')).is_equal_to(fias_suggest_count)
        return self

    @allure.step('Проверка списка с подсказками')
    def choose_address_from_suggest_list(self, value: str):
        self._address_dropdown.choose_suggest(suggest=value)
        return self

    @allure.step('Проверка адреса')
    def assure_address(self, address: AddressFormData):
        self._address_field_input(field="Улица").with_(timeout=5).should(be.clickable)
        with soft_assertions():
            if address.full_address:
                self.assure_search_field(address.full_address)
            if address.country:
                assert_that(self._address_field_input(field="Страна").get(query.value)).contains(address.country)
            if address.subject:
                assert_that(self._address_field_input(field="Субъект").get(query.value)).contains(address.subject)
            if address.city:
                assert_that(self._address_field_input(field="Населенный пункт").get(query.value)).contains(address.city)
            if address.object_:
                assert_that(self._address_field_input(field="Объект").get(query.value)).contains(address.object_)
            if address.admin_area:
                assert_that(self._dropdown_with_text('Округ').text).contains(address.admin_area)
            if address.admin_district:
                assert_that(self._dropdown_with_text('Район').text).contains(address.admin_district)
            if address.street:
                assert_that(self._address_field_input(field="Улица").get(query.value)).contains(address.street)
            if address.house_number:
                assert_that(self._address_field_input(field="Дом/Вл").get(query.value)).contains(address.house_number)
            if address.building:
                assert_that(self._address_field_input(field='Корпус').get(query.value)).contains(address.building)
            if address.housing:
                assert_that(self._address_field_input(field='Стр/соор').get(query.value)).contains(address.housing)
            if address.flat:
                assert_that(self._address_field_input(field='Квартира/офис').get(query.value)).contains(address.flat)
            if address.entrance:
                assert_that(self._address_field_input(field='Подъезд').get(query.value)).contains(address.entrance)
            if address.floor:
                assert_that(self._address_field_input(field='Этаж').get(query.value)).contains(address.floor)
            if address.address_description:
                self.assure_address_description_field(address.address_description)

    @allure.step('Ввести значение в строку поиска')
    def type_value_to_search_field(self, value: str):
        self._address_dropdown.type_value(value=value)
        return self

    @allure.step('Ввести значение в строку поиска с удалением предыдущего значения')
    def set_value_to_search_field(self, value: str):
        self._address_dropdown.set_value(value=value)
        return self

    @allure.step('Проверка подсветки адреса красным')
    def assure_full_address_is_red(self):
        assert_that(get_text_color(self._full_address)).is_equal_to(Color.RED)

    @allure.step('Проверка значения в строке поиска')
    def assure_search_field(self, value: str):
        assert_that(self._full_address.get(query.value)).contains(value)

    @allure.step('Проверка значения в поле Описательный адрес')
    def assure_address_description_field(self, value: str):
        assert_that(self._address_desc.get(query.value).strip()).is_equal_to(value)

    @allure.step('Проверка отсутствия значения в строке поиска')
    def assure_value_not_in_search_field(self, value: str):
        assert_that(self._full_address.get(query.value)).does_not_contain(value)

    @allure.step('Клик по кнопке Совпадение')
    def click_concurrence_button(self):
        from pages.incident_card.custom_elements.modal_windows.accidents_address_repeated_dialog import \
            AccidentsAddressRepeatedDialog
        self._concurrence_btn.click()
        return AccidentsAddressRepeatedDialog(css='#accidentsAddressRepeatedDialog')

    @allure.step('Клик по кнопке Очистить адрес')
    def clean_address(self):
        self._clean_address_btn.with_(timeout=5).should(be.clickable).click()
        return self

    @allure.step('Проверка значения в полях адреса')
    def assure_input_field(self, field: str, value: str):
        assert_that(self._address_field_input(field).get(query.value)).is_equal_to(value)
        return self

    @allure.step('Парсинг, сортировка, проверка опций')
    def assure_parsed_sorted_options(self, dropdown: str):
        options_list_ui = self._dropdown_with_text(dropdown).get_options()
        sorted_options_list_ui = sorted(options_list_ui, key=str.lower)
        assert_that(options_list_ui).is_equal_to(sorted_options_list_ui)

    @allure.step('Проверка сортировки списка значений из дропдауна Округ/Район')
    def assure_dropdown_list_sort(self, dropdown: str, value: str):
        self._dropdown_with_text(dropdown).click()
        self.assure_parsed_sorted_options(dropdown=dropdown)
        self._dropdown_with_text(dropdown).set_value(value)
        self.assure_parsed_sorted_options(dropdown=dropdown)

    @allure.step('Ввод значений в полях адреса')
    def set_values_to_input_fields(self, address: AddressFormData):
        if address.full_address:
            self.set_value_to_search_field(address.full_address)
        if address.country:
            self._address_field_input(field='Страна').set_value(address.country)
        if address.subject:
            self._address_field_input(field='Субъект').clear().set_value(address.subject)
        if address.city:
            self._address_field_input(field='Населенный пункт').set_value(address.city)
        if address.object_:
            self._address_field_input(field='Объект').set_value(address.object_)
        if address.admin_area:
            self._dropdown_with_text('Округ').set_value_with_search_field(value=address.admin_area)
        if address.admin_district:
            self._dropdown_with_text('Район').set_value_with_search_field(value=address.admin_district)
        if address.street:
            self._address_field_input(field='Улица').set_value(address.street)
        if address.house_number:
            self._address_field_input(field='Дом/Вл').set_value(address.house_number)
        if address.building:
            self._address_field_input(field='Корпус').set_value(address.building)
        if address.housing:
            self._address_field_input(field='Стр/соор').set_value(address.housing)
        if address.flat:
            self._address_field_input(field='Квартира/офис').set_value(address.flat)
        if address.entrance:
            self._address_field_input(field='Подъезд').set_value(address.entrance)
        if address.floor:
            self._address_field_input(field='Этаж').set_value(address.floor)
        if address.address_description:
            self._address_desc.set_value(address.address_description)
        self._address_field_input(field='Этаж').click()  # нужно для прогрузки адресов
        return self

    @allure.step('Проверка отсутствия кнопки Совпадение')
    def assure_concurrence_button_is_not_visible(self):
        self._concurrence_btn.should(be.not_.visible)

    @allure.step('Проверка сообщения о том, что адрес не найден в справочнике')
    def assure_address_not_found_message(self):
        self._address_not_found_message.should(be.visible)


class AddressContainerSaved(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._full_address = self.element.s('//*[contains (@class, "view-full")]')
        self._address_desc = self.element.s('//*[contains (@class, "view-description")]')

    @allure.step('Проверка адреса')
    def assure_address(self, address: AddressFormData):
        with soft_assertions():
            if address.full_address:
                custom_full_address = f'{address.country}, {address.subject}, {address.city}, ' \
                                      f'{address.object_}, {address.street}, {address.house_number}'
                assert_that(self._full_address.get(query.text)).contains(custom_full_address)
            if address.address_description:
                assert_that(self._address_desc.get(query.text)).contains(address.address_description)
