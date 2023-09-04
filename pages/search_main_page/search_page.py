from typing import List

import allure
from assertpy import assert_that
from selene import query
from selene.api import s, be, ss

from data.builders.advanced_search_form_builder import AdvancedSearchFormData
from pages.common_page import BaseAppPage
from pages.custom_elements.app_dropdown import MultiSelectDropdown
from pages.custom_elements.app_table import SearchPageTabTable
from pages.custom_elements.app_search_form import SearchForm
from pages.custom_elements.head_menu_navigation import HeadMenuNavigation


class SearchPage(BaseAppPage):

    def __init__(self):
        super().__init__()
        self.url = f'https://{self.conf["stand"]}/#!/search'
        self.search_form = SearchForm(xpath='//form[contains (., "Поиск")]')
        self._accidents_table = s('.md-table')
        self.cards_filter_dropdown = MultiSelectDropdown(xpath='//*[@placeholder="выберите что показывать"]//md-select')
        self.table = SearchPageTabTable(xpath='//table[contains (@class, "md-table")]')

        self.head_menu_navigation = HeadMenuNavigation(css='.head-menu__navigation')

        # форма поиска по параметрам
        # todo вынести форму параметры и ее методы в отдельный элемент parameters - по аналогии с отчётами
        self._incident_id_input = s('.//label[.="по номеру карточки:"]/following-sibling::input')
        self._parameters_dropdowns = lambda label_txt: MultiSelectDropdown(
            xpath=f'//label[.="{label_txt}"]/following-sibling::md-select')
        self._parameters_buttons = lambda btn_txt: s(f'.//button[contains (., "{btn_txt}")]')
        self._options = ss('//div[contains (@class, "md-active md-clickable")]//md-option')

    @allure.step('Отображение таблицы со списком происшествий')
    def check_visibility_accidents_table(self):
        self._accidents_table.with_(timeout=10).should(be.visible)

    @allure.step('Проверка опций в дропдауне фильтра')
    def assure_filter_options(self, options: List):
        options_from_ui = self.cards_filter_dropdown.get_options()
        for option in options:
            assert_that(options_from_ui).contains(option)
        assert_that(len(options_from_ui)).is_equal_to(len(options))

    @allure.step('Заполнение формы параметров')
    def fill_parameters(self, form_data: AdvancedSearchFormData):
        if form_data.user_arm:
            self._parameters_dropdowns(label_txt='по АРМу').choose_values(form_data.user_arm, suggest=True)
            self.catcher_click()
            self._parameters_dropdowns(label_txt='по АРМу').is_not_visible()
        if form_data.status:
            self._parameters_dropdowns(label_txt='статус').choose_values(form_data.status, suggest=True)
            self.catcher_click()
            self._parameters_dropdowns(label_txt='статус').is_not_visible()
        if form_data.incident_id:
            self._incident_id_input.set_value(form_data.incident_id)
        if form_data.group_name:
            self._parameters_dropdowns(label_txt='по группе').choose_values(form_data.group_name)
            self.catcher_click()
            self._parameters_dropdowns(label_txt='по группе').is_not_visible()
        return self

    @allure.step('Проверка значений в дропдауне параметров')
    def assure_parameters_dropdown_options(self, parameter_dropdown_text: str, option: str, is_visible: bool):
        self._parameters_dropdowns(label_txt=parameter_dropdown_text).click()
        options_list = [option.get(query.text) for option in self._options]
        if is_visible:
            assert_that(options_list).contains(option)
        else:
            assert_that(options_list).does_not_contain(option)

    @allure.step('Клик по кнопке "Сбросить"')
    def reset_form(self):
        self._parameters_buttons(btn_txt='сбросить').click()
        return self

    @allure.step('Клик по кнопке "Искать по параметрам"')
    def search_by_parameters_button_click(self):
        self._parameters_buttons(btn_txt='искать по параметрам').click()
        self.table.wait_loading()
        return self

    @allure.step('Клик по кнопке "Сбросить" параметры')
    def reset_parameters_button_click(self):
        self._parameters_buttons(btn_txt='сбросить').click()
        return self
