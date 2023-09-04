import allure
from selenium.webdriver.common.keys import Keys

from data.buttons import Buttons
from data.titles import Titles
from pages.common.base_element import BaseElement


class SaveIncidentWithoutAnswersWindow(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 's']
        self._title = self.element.s(f'//h1[text() = "{Titles.SAVE_CARD_WITHOUT_DESCRIPTION}"]')
        self._save_btn = self.element.s(f'.//button[text() = "{Buttons.SAVE_CARD}"]')
        self._return_and_fill_btn = self.element.s(f'.//button[text() = "{Buttons.RETURN_AND_FILL_CARD}"]')

    @allure.step('Нажать на кнопку Сохранить карточку')
    def click_save_card_button(self):
        from pages.incident_card.saved_accident_сard_page import SavedAccidentCardPage
        self._save_btn.click()
        return SavedAccidentCardPage()
