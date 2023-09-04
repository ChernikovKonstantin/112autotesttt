import allure
from selene import be
from selene.support.shared.jquery_style import s

from pages.common.base_element import BaseElement


class HeadMenuNavigation(BaseElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # вкладки
        self._classifiers_manager_page_link = s('//a[@href="#!/classifiersManager"]')
        self._shift_management_page_link = s('//a[@href="#!/shiftManagement"]')
        self._search_page_link = s('//a[@href="#!/search"]')

    @allure.step('Перейти на вкладку "УЕР"')
    def go_to_classifiers_manager_page(self):
        from pages.classifiers_manager.classifiers_manager_page import ClassifiersManagerPage
        self._classifiers_manager_page_link.with_(timeout=20).should(be.clickable).click()
        return ClassifiersManagerPage()

    @allure.step('Перейти на вкладку "Смена"')
    def go_to_shift_management_page(self):
        from pages.shift_managment.shift_management_page import ShiftManagementPage
        self._shift_management_page_link.with_(timeout=20).should(be.clickable).click()
        return ShiftManagementPage()

    @allure.step('Перейти на вкладку "Смена"')
    def go_to_search_page(self):
        from pages.search_main_page.search_page import SearchPage
        self._search_page_link.should(be.clickable, timeout=5).click()
        return SearchPage()
