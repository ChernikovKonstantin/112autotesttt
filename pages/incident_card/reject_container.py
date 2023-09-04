from selenium.webdriver.common.keys import Keys
from pages.incident_card.base_container import BaseContainer


class RejectContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 'n']
        self._no_contact_btn = self.element.s('//button[contains (text(), "нет контакта")]')
        self._fail_call_btn = self.element.s('//button[contains (text(), "срыв звонка")]')
        self._elements_for_assert = [self._no_contact_btn, self._fail_call_btn]
