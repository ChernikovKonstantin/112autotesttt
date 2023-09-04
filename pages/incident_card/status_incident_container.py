import allure

from pages.common.base_element import BaseElement


class StatusIncidentContainer(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._reporting_accepted_btn = self.element.s('//button[normalize-space()="нарушения исправлены"]')

    @allure.step("Нажать на кнопку 'Нарушения исправлены'")
    def click_reporting_accepted_button(self):
        self._reporting_accepted_btn.click()
        return self
