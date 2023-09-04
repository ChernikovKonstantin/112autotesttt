import allure
from assertpy import assert_that
from selene import be

from pages.common.base_element import BaseElement


class DeleteErrorDialog(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ok_btn = self.element.s('.//button[.="OK"]')
        self._p_with_text = self.element.s('.//p[.="Полигон, привязанный к службе, нельзя удалить"]')

        self.waiting_to_be_visible(timeout=10)

    @allure.step('Клик по кнопке OK')
    def click_ok_button(self):
        from pages.classifiers_manager.polygon_reaction_page import PolygonReactionPage
        self._ok_btn.click()
        return PolygonReactionPage()

    @allure.step('Проверка отображения текста сообщения')
    def assert_message_text(self):
        self._p_with_text.should(be.visible)
