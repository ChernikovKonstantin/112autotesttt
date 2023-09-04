from assertpy import assert_that, soft_assertions
from selenium.webdriver.common.keys import Keys

import allure
from selene.api import query

from data.users.user_list import User
from pages.common.base_element import BaseElement
from pages.incident_card.base_container import BaseContainer


class IncidentDescriptionContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 'o']
        self._char_counter = self.element.s('div .md-char-counter')
        self._textarea = self.element.s('//md-input-container/textarea')

    @allure.step('Заполнить поле "Описание со слов зявителя"')
    def fill_description(self, desc: str):
        self._textarea.type(desc)

    @allure.step('Проверка счётчика символов')
    def assert_char_counter(self, desc: str):
        assert_that(self._char_counter.get(query.text)).is_equal_to(f'{len(desc)} / 1999')


class IncidentDescriptionContainerSaved(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._author = self.element.s('//*[contains (@class, "item__author")]')
        self._description = self.element.s('//*[contains (@class, "item__description")]')

    @allure.step('Проверка текста и автора')
    def assure_block(self, user: User, desc: str):
        with soft_assertions():
            assert_that(self._author.get(query.text)).contains(user.name_with_dots)
            assert_that(self._description.get(query.text)).contains(desc)
