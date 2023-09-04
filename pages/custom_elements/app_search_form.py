import allure
from selene import be
from pages.common.base_element import BaseElement


class SearchForm(BaseElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._input = self.element.s('.//input')
        self._submit_btn = self.element.s('.//button[@type="submit"]')
        self._advanced_search_btn = self.element.s('.//*[@role="button" and contains(., "расширенный по параметрам")]')
        self._arrow_down_icon = self._advanced_search_btn.s('./i[.="keyboard_arrow_down"]')

    @allure.step('Открытие формы поиска по параметрам')
    def open_advanced_form(self):
        self._advanced_search_btn.click()
        self._arrow_down_icon.should(be.not_.visible)
        return self

    @allure.step('Ввод значения и поиск')
    def set_value_and_search(self, value):
        self._input.set_value(value)
        self._submit_btn.click()
        return self
