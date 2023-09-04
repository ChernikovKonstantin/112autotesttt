import allure
from selene import be
from selenium.webdriver.common.keys import Keys

from pages.incident_card.base_container import BaseContainer


class InjuredContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 'p']
        self._injured_btn = self.element.s('//button[contains (text(), "Пострадавшие")]')
        self._refuse_ambulance_btn = self.element.s('//button[contains (text(), "Нет на месте")]')
        self._blocked_btn = self.element.s('//button[contains (text(), "Нет доступа")]')
        self._injured_count_input = self.element.s('.//input')
        self._elements_for_assert = [self._injured_btn, self._refuse_ambulance_btn, self._blocked_btn]

    @allure.step('Проверка активации инпута для ввода кол-ва пострадавших')
    def assure_activate_count_input(self):
        self._injured_count_input.should(be.not_.visible)
        self._injured_btn.press_enter()
        self._injured_count_input.should(be.visible)
