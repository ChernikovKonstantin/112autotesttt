from typing import List

import allure
from assertpy import soft_assertions, assert_that
from selene import be, have
from selenium.webdriver.common.keys import Keys

from pages.common.base_element import BaseElement
from pages.custom_elements.app_dropdown import DropDownSuggest
from pages.incident_card.base_container import BaseContainer
from selene_custom import query


class WhatHappensContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 't']
        self._what_happens_title = self.element.s('//label[text()="Введите тип происшествия"]')
        self._what_happens_dropdown = DropDownSuggest(xpath='//*[@aria-label="что случилось?"]')
        self._what_happens_buttons = self.element.ss('//*[contains (@class, "buttons-container")]//button')
        self._important_answers_title = self.element.s(
            '//*[@id="important-answers-container"]/div[text()="Значимые типы проишествий:"]')
        self._important_answers_buttons = self.element.ss('//*[@id="important-answers-container"]//button')
        self._elements_for_assert = [self._what_happens_title,
                                     self._important_answers_title,
                                     ]

    @allure.step('Проверка часто выбираемых тегов и значимых типов происшествий')
    def assure_answers(self, answers: List, important_answers: List):
        ui_what_happens_answers = [button.get(query.text) for button in self._what_happens_buttons]
        ui_what_happens_important_answers = [button.get(query.text) for button in self._important_answers_buttons]
        with soft_assertions():
            for answer in answers:
                assert_that(ui_what_happens_answers).contains(answer)
            for important_answer in important_answers:
                assert_that(ui_what_happens_important_answers).contains(important_answer)

    @allure.step('Выбор типа инцидента')
    def choose_incident_type(self, incident: str):
        self._what_happens_dropdown.set_partial_value_and_choose_suggest(value=incident)
        return self

    @allure.step('Выбор тэга инцидента')
    def choose_incident_tag(self, tag_name: str):
        self._what_happens_buttons.element_by(have.text(tag_name)).click()
        return self

    @allure.step('Проверка: блок не отображается')
    def assure_block_not_visible(self):
        self.element.should(be.not_.visible)


class WhatHappensContainerSaved(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._item_containers = self.element.ss('//*[contains (@class, "item-container")]')
        self._first_item_container_answers = self._item_containers[0].ss('.//span[@class="bold-answer"]')

    @allure.step('Проверка ответов')
    def assure_answers(self, answers: List):
        ui_what_happens_answers = ','.join(
            [answer.get(query.text).lower() for answer in self._first_item_container_answers])
        with soft_assertions():
            for answer in answers:
                assert_that(ui_what_happens_answers).contains(answer.lower())

    @allure.step('Проверка количества блоков вопросов касательно инцидентов')
    def assure_count_items(self, count: int):
        assert_that(len(self._item_containers)).is_equal_to(count)
