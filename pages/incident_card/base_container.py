import allure
from assertpy import soft_assertions, assert_that
from selene import have, be
from selene.support.shared.jquery_style import s

from pages.common.base_element import BaseElement


class BaseContainer(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = []
        self._elements_for_assert = []

    @allure.step('Активация контейнера при помощи клавиатуры')
    def activate_by_keyboard(self):
        s('//body').press(self._keyboard_combinations)
        self.element.with_(timeout=10).should(have.css_class('highlight-active'))
        return self

    @allure.step('Проверка видимости элементов')
    def assure_elements_is_visible(self):
        with soft_assertions():
            for elem in self._elements_for_assert:
                assert_that(elem.with_(timeout=10).matching(be.visible)).is_true()

    @allure.step('Нажать кнопку TAB')
    def push_tab(self):
        self.element.s('//body').press_tab()
        return self
