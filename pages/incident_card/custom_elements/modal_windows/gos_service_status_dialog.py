import allure

from pages.common.base_element import BaseElement
from pages.custom_elements import AppDropdown


class GosServiceStatusDialog(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._status = AppDropdown(xpath='//label[.="Статус"]/following-sibling::md-select')
        self._save_btn = self.element.s('.//button[contains(., "done")]')

    @allure.step('Выбор статуса в дропдауне')
    def choose_status(self, status: str):
        self._status.choose_value(value=status)
        return self

    @allure.step('Клик по кнопке "Сохранить"')
    def click_save_button(self):
        from pages.incident_card.saved_accident_сard_page import SavedAccidentCardPage
        self._save_btn.click()
        return SavedAccidentCardPage()
