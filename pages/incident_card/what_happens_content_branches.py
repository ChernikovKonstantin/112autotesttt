from typing import List

import allure
from assertpy import assert_that, soft_assertions
from selene import be
from selene.core.entity import Element
from selenium.webdriver.common.keys import Keys

from data.color_data import Color
from pages.incident_card.base_container import BaseContainer
from selene_custom import query
from utils.service_utils import get_background_color, get_outline_color


class BaseBranch(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._list_item = self.element.ss('//div[contains (@class, "incident-content__question-list-item")]')
        self._link = self.element.s('//a')
        self._button = lambda button: self._element.s(f'//button[contains (text(), "{button}")]')
        self._answer_buttons = self.element.ss('.//div[contains (@class, "answer-list")]/button')
        self._elements_for_assert = [
            self._list_item,
        ]

    @allure.step('Проверка контента уточняющих вопросов')
    def assure_content(self, incident_content: List):
        content_items_ui = [item.get(query.text) for item in self._list_item]
        with soft_assertions():
            for item in incident_content:
                assert_that(content_items_ui).contains(item)

    @allure.step('Выбор ответов')
    def choose_answers(self, buttons: List):
        for button in buttons:
            self._button(button).click()
        return self

    @staticmethod
    @allure.step('Проверка кнопка активна')
    def _check_button_is_active(button: Element):
        assert_that(button.with_(timeout=10).get(query.class_value)).contains('active')
        assert_that(get_background_color(button)).is_equal_to(Color.BLUE)

    @allure.step('Проверка ответов')
    def check_answers_active_buttons(self, buttons: List):
        with soft_assertions():
            for button in buttons:
                self._check_button_is_active(button=self._button(button))

    @allure.step('Проверка фокуса на ответе')
    def assure_answer_in_focus(self, answer_number: int):
        assert_that(get_outline_color(self._answer_buttons[answer_number - 1])).is_equal_to(Color.OUTLINE_COLOR_BLUE)

    @allure.step('Выбрать первый ответ на котором фокус')
    def choose_first_answer_with_focus_by_keyboard(self):
        self._answer_buttons[0].press(Keys.SPACE)
        return self

    @allure.step('Проверка: ответ выбран')
    def assure_answer_is_selected(self, answer_number: int):
        self._check_button_is_active(self._answer_buttons[answer_number - 1])

    @allure.step('Проверка заголовка ветки')
    def assure_branch_title(self, branch_title):
        assert_that(self._link.get(query.text)).contains(branch_title)

    @allure.step('Проверка: ветка отображается')
    def assure_branch_is_visible(self):
        assert_that(self.element.matching(be.visible)).is_true()

    @allure.step('Проверка: ветка не отображается')
    def assure_branch_is_not_visible(self):
        assert_that(self.element.matching(be.not_.visible)).is_true()


class FirstBranch(BaseBranch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, '1']


class SecondBranch(BaseBranch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, '2']


class ThirdBranch(BaseBranch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, '3']
