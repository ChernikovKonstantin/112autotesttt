import allure
from selene.api import s

from conf.conf import Conf
from data.users.user_list import User
from pages.common_page import BaseAppPage
from pages.search_main_page.search_page import SearchPage


class LoginPage(BaseAppPage):
    url_pattern = 'https://{ip}/#!/login'

    def __init__(self, window_id=None):
        super().__init__()
        self.conf = Conf.configuration
        self._window_id = window_id
        self.url = self.url_pattern.format(ip=self.conf['stand'])
        self._login = s('#user')
        self._password = s('#password')
        self._arm_number = s('#workPlace')
        self._login_btn = s("button[type='submit']")
        self.navigate()

    @allure.step('Заполнить форму авторизации')
    def fill_form(self, login, password, arm):
        self._login.set_value(login)
        self._password.set_value(password)
        self._arm_number.set_value(arm)

    @allure.step('Нажатие кнопки "Войти"')
    def click_on_login_button(self):
        self._login_btn.click()

    @allure.step('Авторизация в системе в ИС ПРО')
    def login(self, user: User):
        self.fill_form(user.login, user.password, user.arm)
        self.click_on_login_button()
        self.wait_for_loading()
        return SearchPage()
