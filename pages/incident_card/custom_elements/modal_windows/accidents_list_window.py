import allure
from assertpy import assert_that
from selene import be
from selene.support.shared.jquery_style import s
from selenium.webdriver.common.keys import Keys

from pages.common.base_element import BaseElement


class AccidentsListWindow(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 'w']
        self._content_search_block = self.element.s('//*[contains (@class, "content__search")]')
        self._content_accidents_block = self.element.s('//*[contains (@class, "content__accidents")]')
        self._return_to_card_button = self.element.s(f'.//button[contains (., "вернуться в карточку")'
                                                     f' and contains (@class, "focus-element")]')
        self._input_date_focus_element = s('//*[@id="filters-dates1"]/input[contains (@class, "focus-element")]')
        self._expands_details_focus_element = self.element.ss('//td[contains (@class, "focus-element")]')
        self._footer = self.element.s('//*[contains (@class, "footer incident")]')

    @allure.step('Открытие окна создания связей при помощи клавиатуры')
    def open_window_by_keyword(self):
        s('//body').press(self._keyboard_combinations)
        return self

    @allure.step('Активация блока поиска просишествия')
    def activate_content_search_block(self):
        self.element.s('//body').press(Keys.ALT, 1)
        return self

    @allure.step('Проверка наличия инпута времени')
    def assure_time_input_is_enabled(self):
        assert_that(self._input_date_focus_element.matching(be.enabled)).is_true()

    @allure.step('Активация блока списка проишествия')
    def activate_content_accidents_block(self):
        self.element.s('//body').press(Keys.ALT, 2)
        return self

    @allure.step('Проверка видимости элемента раскрытия блока с подробной информацией')
    def assure_expands_details_is_visible(self):
        self._expands_details_focus_element[0].should(be.visible, timeout=5)

    @allure.step('Активация футера')
    def activate_footer(self):
        self.element.s('//body').press(Keys.ALT, 3)
        return self

    @allure.step('Проверка видимости футера')
    def assure_footer_is_enabled(self):
        assert_that(self._footer.matching(be.enabled)).is_true()

    @allure.step('Нажать на кнопку Вернуться в карточку')
    def click_return_to_card_button(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self._return_to_card_button.click()
        return NewAccidentCardPage()

    @allure.step('Вернуться в карточку нажатием Enter в активированном футере')
    def return_to_card_by_keyboard(self):
        from pages.incident_card.new_accident_card_page import NewAccidentCardPage
        self.activate_footer()
        self._return_to_card_button.press_enter()
        return NewAccidentCardPage()
