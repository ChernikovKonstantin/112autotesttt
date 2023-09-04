import allure
from assertpy import assert_that, soft_assertions
from selene import be, have, query
from selene.core import command
from selene.support.shared.jquery_style import s

from data.builders.workoff_builder import WorkoffFormData
from data.dates import is_datetime_between_dates_with_delta
from pages.common.base_element import BaseElement
from pages.custom_elements.app_dropdown import MultiSelectDropdown, AppDropdown
from pages.search_main_page.modal_windows.change_status_modal_window import ChangeStatusModalWindow

from selene.support.shared import browser
from selenium.webdriver import ActionChains


class AppTable(BaseElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._visible_progress_linear = self.element.s('.//md-progress-linear[@aria-hidden="false"]')
        self._table_rows = self.element.ss('//tbody/tr')
        self._edit_button_in_row_with_text = lambda row_text: self.element.s(
            f'//td/div[contains (., "{row_text}")]/following::button[@title="Редактировать"]')
        self._save_button_in_row_with_text = lambda row_text: self.element.s(
            f'//td/div[contains (., "{row_text}")]/following::button[@title="Сохранить"]')
        self._tooltip = self.element.s('//md-tooltip')

    @allure.step('Ожидание прогрузки таблицы')
    def wait_loading(self):
        try:
            self._visible_progress_linear.with_(timeout=5).should(be.visible).with_(timeout=5).should(be.not_.visible)
        except Exception as e:
            print('Элемент прогрузки таблицы не найден, ошибка: ', e)
        return self

    @allure.step('Проверка: строка содержит значение')
    def assure_row_contains_value(self, expected: str, row_number: int):
        self._table_rows[row_number - 1].should(have.text(expected), timeout=10)

    @allure.step('Клик по кнопке редактирования в строке с текстом')
    def click_edit_button_in_row_contains_text(self, row_text: str):
        self._edit_button_in_row_with_text(row_text=row_text).click()
        return self

    @allure.step('Клик по кнопке сохранения в строке с текстом')
    def click_save_button_in_row_contains_text(self, row_text: str):
        self._save_button_in_row_with_text(row_text=row_text).perform(command.js.click).should(be.not_.visible,
                                                                                               timeout=5)
        return self


class GosServicesTabTable(AppTable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._districts_dropdown = MultiSelectDropdown(xpath='//div[contains(@class, "gos-service-list")]//md-select')
        self._districts_column = self.element.s('.//td[contains (@class, "district")]')

    @allure.step('Добавить район выезда на вкладке Справочник служб')
    def add_district(self, name: str):
        self._districts_dropdown.choose_values(name)
        return self

    @allure.step('Проверка: Колонка "Районы выезда" содержит tooltip')
    def assure_districts_have_tooltip(self, tooltip: str):
        self._districts_column.should(be.clickable, timeout=5)
        ActionChains(browser.driver).move_to_element(self._districts_column()).perform()
        ui_tooltips = self._tooltip.should(be.visible, timeout=5).get(query.text)
        assert_that(ui_tooltips).contains(tooltip)


class SearchPageTabTable(AppTable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._table_rows = self.element.ss('//tbody/tr[contains (@style, "background")]')
        self._edit_service_btn = lambda incident_id: self.element.s(
            f'//tr[contains(., "{incident_id}")]//i[contains (., "mode_edit")]')
        self._expand_detail_btn = lambda incident_id: self.element.s(
            f'//tr[contains(., "{incident_id}")]//td[contains (@class, "expand-details")]')
        self._final_status_tooltip = self.element.s(
            './following::*/md-tooltip[contains (., "Выставлен конечный статус")]')
        self._workoff_item_last = s('//div[contains(@class, "workoff-item")][last()]')

    @allure.step('Клик по кнопке изменить статус службы')
    def click_edit_service_status_button_for_incident(self, incident_id: str):
        self._edit_service_btn(incident_id=incident_id).perform(command.js.click)
        return ChangeStatusModalWindow(css='#newGosServiceStatus')

    @allure.step('Проверка отображения tooltip')
    def assure_final_status_tooltip_for_incident_is_visible(self, incident_id: str):
        ActionChains(browser.driver).move_to_element(self._edit_service_btn(incident_id=incident_id)()).perform()
        self._final_status_tooltip.should(be.visible)

    @allure.step('Раскрытие блока деталей для инцидента {incident_id}')
    def expand_details_for_incident(self, incident_id: str):
        self._expand_detail_btn(incident_id=incident_id).should(be.clickable, timeout=5).click()
        return self

    @allure.step('Проверка информации по последней отработке')
    def assure_incident_last_workoff_data(self, form_data: WorkoffFormData):
        workoff_data_from_ui = self._workoff_item_last.get(query.text)
        operator = f'Оп. {form_data.operator_id} в '
        with soft_assertions():
            for value in (operator,
                          form_data.service,
                          form_data.call_destination,
                          form_data.phone_humber,
                          form_data.username,
                          form_data.description):
                assert_that(workoff_data_from_ui).contains(value)
            assert_that(is_datetime_between_dates_with_delta(date=form_data.save_workoff_time,
                                                             minutes_delta=3)).is_true()


class ClassifiersManagerTabTable(AppTable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._edit_button_in_row_with_text = lambda row_text: self.element.s(
            f'.//tr[contains (., "{row_text}")]//td//i[.="mode_edit"]')
        self._save_button_in_row_with_text = lambda row_text: self.element.s(
            f'.//tr[contains (., "{row_text}")]//td//i[.="done"]')
        self._add_service_btn = self.element.s('//td/button[contains (@class, "action-add-service")]')
        self._gos_service_dropdown = AppDropdown(xpath='//md-select[@ng-model="govService.govService"]')
        self._service_conditions_dropdown = MultiSelectDropdown(
            xpath='//md-select[@ng-model="govService.tempConditions"]')

    @allure.step('Нажатие кнопки Добавить службу')
    def click_add_service_button(self):
        self._add_service_btn.should(be.clickable, timeout=5).click()
        return self

    @allure.step('Редактирование классификатора')
    def edit_classifier(self, gos_service: str, service_condition: str):
        self._gos_service_dropdown.choose_value(gos_service)
        self._service_conditions_dropdown.choose_values(service_condition)
        return self
