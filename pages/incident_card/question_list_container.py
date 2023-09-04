import allure
from selenium.webdriver.common.keys import Keys

from pages.custom_elements.app_dropdown import DropDownSuggest
from pages.incident_card.base_container import BaseContainer


class QuestionListContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 't']
        self._input = self.element.s('//input[@placeholder="добавить тип происшествия"]')
        self._autocomplete_dropdown = DropDownSuggest(xpath='//*[@aria-label="добавить тип происшествия"]')
        self._elements_for_assert = [
            self._input,
        ]

    @allure.step('Добавление типа инцидента')
    def add_incident_type(self, incident: str):
        self._autocomplete_dropdown.set_partial_value_and_choose_suggest(value=incident)
