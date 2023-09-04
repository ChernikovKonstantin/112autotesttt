import allure
from assertpy import soft_assertions, assert_that

from pages.common.base_element import BaseElement
from selene.api import be

from selene_custom import query


class TimerContainer(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._indicator = self.element.s('.indicator')
        self._indicator_mm = self.element.s('.title-mm')
        self._indicator_ss = self.element.s('.title-ss')

    @allure.step('Проверка блока Таймер')
    def elements_is_visible(self):
        with soft_assertions():
            assert_that(self._indicator.matching(be.visible)).is_true()
            assert_that(self._indicator_mm.get(query.text)).is_equal_to('минут')
            assert_that(self._indicator_ss.get(query.text)).is_equal_to('секунд')
