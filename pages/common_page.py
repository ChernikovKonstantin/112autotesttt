import allure
from selene import be
from selene.core import command
from selene.support.shared.jquery_style import s
from selenium.webdriver.common.keys import Keys

from conf.conf import Conf
from pages.base_page import BasePage


class BaseAppPage(BasePage):

    def __init__(self, window_id=None):
        super().__init__()
        self.conf = Conf.configuration
        self._window_id = window_id
        self._new_card_button = s('//button[contains(@class, "new-card-button")]')
        self._exit_btn = s('//*[contains(@class, "current-user-exit")]')
        self._click_catcher = s('//*[contains (@class, "md-click-catcher")]')

    @allure.step('Перейти на страницу создания карточки происшествия')
    def go_to_new_card_page(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self._new_card_button.with_(timeout=20).should(be.clickable).click()
        return NewAccidentCardPage()

    @allure.step('Перейти на страницу создания карточки происшествия при помощи клавиатуры')
    def go_to_new_card_page_by_keyboard(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self.wait_for_loading()
        s('//body').press(Keys.INSERT)
        return NewAccidentCardPage()

    @allure.step('Выйти и вернуться на экран авторизации')
    def logout(self):
        self._exit_btn.with_(timeout=20).should(be.clickable).click()

    @allure.step('Клик по элементу отслеживания клика')
    def catcher_click(self):
        self._click_catcher.should(be.clickable, timeout=5).perform(command.js.click)
        return self

    @allure.step('Открытие страницы инцидента')
    def go_to_incident_page(self, incident_id):
        from pages.incident_card.saved_accident_сard_page import SavedAccidentCardPage
        self.open_page(url=f'/#!/incident/{incident_id}/search/')
        return SavedAccidentCardPage()
