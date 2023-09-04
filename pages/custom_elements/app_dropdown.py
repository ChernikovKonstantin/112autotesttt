from __future__ import annotations

from typing import Optional, List

import allure
from assertpy import assert_that
from selene import be
from selene.api import ss, have, command, s

from data.color_data import Color
from pages.common.base_element import BaseElement
from selene_custom import query
from utils.service_utils import get_int_from_text, get_background_color, wait_seconds


class AppDropdown(BaseElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._selected_option = self._element.s('.md-select-value > span')
        self._options = ss('//div[contains (@class, "md-active md-clickable")]//md-option')
        self._md_option_leave_active = s(
            '//div[contains (@class, "md-active md-clickable")]//md-option[contains (@class, "leave-active")]')
        self._x_icon = self._element.s('.clear-icon')
        self._search_field = s('//div[contains (@class, "md-active md-clickable")]//input')

    @property
    def text(self):
        return self._selected_option.get(query.text)

    def set_value(self, value: Optional[str]) -> AppDropdown:
        self.element.click()
        self._search_field.set_value(value)
        self._md_option_leave_active.should(be.not_.visible, timeout=5)
        return self

    def choose_value(self, value: Optional[str]) -> AppDropdown:
        wait_seconds(0.6)  # анимация дропдауна долго отрабатывает
        if value is not None:
            self.element.click()
            self._options.element_by(have.text(value)).with_(timeout=6).perform(command.js.scroll_into_view).click()
            self._options.should(be.hidden)
        return self

    def choose_value_from_open_dropdown(self, value: str) -> AppDropdown:
        self._options[0].should(be.visible, timeout=5)
        element = self._options.with_(timeout=2).element_by(have.text(value))
        element.click()
        self._options.should(be.hidden)
        return self

    def set_value_with_search_field(self, value: Optional[str]) -> AppDropdown:
        if value is not None:
            self._element.with_(timeout=10).click()
            self._search_field.set_value(value[:2])
            element = self._options.with_(timeout=10).element_by(have.text(value))
            element.click()
            self._search_field.should(be.hidden)
        return self

    def get_options(self):
        self._options[0].with_(timeout=10).should(be.visible)
        option_list = [option.get(query.text) for option in self._options]
        self._options[0].press_escape()
        self._options.should(be.not_.visible, timeout=5)
        return option_list

    def options_is(self, visible: bool):
        if visible:
            self._options.should(be.visible)
        else:
            self._options.should(be.not_.visible)


class DropDownSuggest(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._options = self.element.ss('//*[@class="md-autocomplete-suggestion"]')
        self._matches_count = self.element.s('//div[@class="md-visually-hidden"]')

    def set_value(self, value: Optional[str]) -> DropDownSuggest:
        self.element.set_value(value)
        self._options[0].with_(timeout=10).should(be.visible)
        return self

    def type_value(self, value: Optional[str]) -> DropDownSuggest:
        self.element.type(value)
        self._options[0].with_(timeout=10).should(be.visible)
        return self

    def scroll_to_end_suggest_list(self) -> DropDownSuggest:
        matches_count = get_int_from_text(self._matches_count.get(query.text))
        for i in range(matches_count // len(self._options)):
            self._options[len(self._options) - 1].perform(command.js.scroll_into_view)
        return self

    def get_last_suggestions(self) -> List:
        return [suggest.get(query.text) for suggest in self._options]

    def choose_suggest(self, suggest: str) -> DropDownSuggest:
        self._options.element_by(have.text(suggest)).click()
        self._options.with_(timeout=5).should(be.not_.visible)
        return self

    def set_partial_value_and_choose_suggest(self, value: Optional[str]) -> DropDownSuggest:
        if value is not None:
            self._element.with_(timeout=10).click()
            self.element.set_value(value[:2])
            self.choose_suggest(suggest=value)
        return self


class MultiSelectDropdown(AppDropdown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def assure_values(self, *values: Optional[List[str], str]):
        for value in values:
            assert_that(self.element.get(query.text)).contains(value)

    def deselect(self):
        self._element.should(be.clickable, timeout=5).click()
        self._options[0].should(be.clickable)
        for option in self._options:
            option.click() if option.get_attribute('aria-selected') == 'true' else None
        return self

    @allure.step('Выбрать значения в дропдауне')
    def choose_values(self, *values: Optional[List[str], str], suggest: bool = False) -> MultiSelectDropdown:
        self._element.should(be.clickable, timeout=5).click()
        for value in values:
            if suggest:
                self._search_field.set_value(value)
            element = self._options.element_by(have.text(value))
            element.click()
            wait_seconds(0.3)
            assert_that(get_background_color(element)).is_equal_to(Color.BLUE)
        return self
