import allure
from selene.api import s, be, browser
from pprint import pformat
from selene.core.entity import Element
from selene.core.exceptions import TimeoutException
from waiting import wait, TimeoutExpired

from utils.common_check import assure_current_page_url_contains_text

from utils.service_utils import wait_seconds


class BasePage:
    """
    Базовый класс для страниц приложения
    """

    def __init__(self):
        self.url = ""
        self.loader = s("#progress-loader")

    @allure.step("Проверка элемента на видимость")
    def check_element_visibility(self, element: Element, is_visible: bool = True, timeout: int = 10):
        try:
            element.with_(timeout=timeout).should(be.visible) if is_visible \
                else element.with_(timeout=timeout).should(be.not_.visible)
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить элемент на активность")
    def check_element_enable(self, element: Element, is_enabled: bool = True, timeout: int = 10):
        try:
            element.with_(timeout=timeout).should(be.enabled) if is_enabled \
                else element.with_(timeout=timeout).should(be.not_.enabled)
            return True
        except TimeoutException:
            return False

    @allure.step('Ожидание прогрузки страницы')
    def wait_for_loading(self, timeout: int = 15):
        if self.check_element_visibility(self.loader, timeout=5):
            self.loader.with_(timeout=timeout).should(be.not_.visible)

    @staticmethod
    def assure_page_opening(expected: str, timeout: int = 4):
        assure_current_page_url_contains_text(expected, timeout=timeout)

    @staticmethod
    def xprint(text: str, allure_title: str = "Комментарий"):
        """
        Вывод текста в консоль + attach в allure
        :param text: текст для вывода
        :param allure_title: метка в allure
        """
        formatted_text = pformat(text)
        allure.attach(formatted_text, allure_title, allure.attachment_type.TEXT)
        print(text)

    @staticmethod
    @allure.step('Обновить страницу')
    def refresh():
        browser.driver.refresh()

    @staticmethod
    @allure.step('Открыть пустую страницу')
    def open_blank_page():
        browser.open('about:blank')

    @staticmethod
    @allure.step('Нажать кнопку подтверждения в окне с алертом')
    def confirm_alert():
        alert = browser.driver.switch_to.alert
        alert.accept()

    @allure.step('Нажать кнопку отмены в окне с алертом')
    def dismiss_alert(self):
        alert = browser.driver.switch_to.alert
        alert.dismiss()
        return self

    @allure.step('Проверка отображения окна с алертом')
    def assure_alert_is_visible(self, message: str):
        alert = browser.driver.switch_to.alert
        assert alert.text == message

    def navigate(self):
        with allure.step('Переход по адресу: "%s"' % self.url):
            browser.open(self.url)
        return self

    @allure.step("Загрузить документ")
    def upload_file(self, input_fld: Element, file_path: str):
        input_fld().send_keys(file_path)

    @staticmethod
    @allure.step('Переход к новой вкладке в браузере')
    def switch_to_another_tab():
        current_tab = browser.driver.current_window_handle
        try:
            wait(lambda: len(browser.driver.window_handles) == 2, timeout_seconds=5)
            all_tabs = browser.driver.window_handles
            all_tabs.remove(current_tab)
            new_tab = all_tabs[0]
            browser.driver.switch_to.window(new_tab)
        except TimeoutExpired:
            raise AssertionError('Two tabs must be present')

    @allure.step('Закрыть все вкладки, кроме текущей')
    def close_other_tabs(self):
        for _ in range(10):
            wait_seconds(0.3)
            if len(browser.driver.window_handles) > 2:
                break
        all_tabs = browser.driver.window_handles
        current_tab = browser.driver.current_window_handle
        all_tabs.remove(current_tab)
        for tab in all_tabs:
            browser.driver.switch_to.window(tab)
            browser.close()
        browser.driver.switch_to.window(current_tab)
        return self

    @staticmethod
    @allure.step('Получить заголовок страницы')
    def get_browser_title():
        return browser.title()

    @staticmethod
    @allure.step('Открыть страницу')
    def open_page(url: str):
        browser.open(url)
