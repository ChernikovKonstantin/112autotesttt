import allure
from assertpy import soft_assertions, assert_that
from selene import be
from selene.support.shared.jquery_style import s
from selenium.webdriver.common.keys import Keys

from data.buttons import Buttons
from pages.common.base_element import BaseElement


class AddedButNotSaveWindow(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.SHIFT, Keys.F1]
        self._title = self.element.s('.//h2["Внимание!"]')
        self._first_modal_info = self.element.s('//div[text() = "Данные карточки были дополнены, но не сохранены."]')
        self._second_modal_info = self.element.s(
            "//div[text() = 'Для сохранения внесенных данных нажмите на кнопку \"Сохранить\"']")
        self._return_to_adding_btn = self.element.s(f'//button[text() = "{Buttons.RETURN_TO_ADDING}"]')
        self._continue_without_saving_btn = self.element.s(f'.//button[text() = "{Buttons.CONTINUE_WITHOUT_SAVING}"]')

    @allure.step('Открытие окна закрытия карточки без сохранения')
    def open_window_by_keyword(self):
        s('//body').press(self._keyboard_combinations)
        return self

    @allure.step('Проверка элементов модального окна с предупреждением что дополнения не сохранены')
    def assure_elements_is_visible(self):
        with soft_assertions():
            with allure.step('Проверка заголовка окна'):
                assert_that(self._title.matching(be.visible)).is_true()
            with allure.step('Проверка отображаемой информации'):
                assert_that(self._first_modal_info.matching(be.visible)).is_true()
                assert_that(self._second_modal_info.matching(be.visible)).is_true()
            with allure.step('Проверка кнопок'):
                assert_that(self._return_to_adding_btn.matching(be.visible)).is_true()
                assert_that(self._continue_without_saving_btn.matching(be.visible)).is_true()

    @allure.step('Нажать кнопку "Вернуться к дополнению"')
    def click_return_to_adding_button(self):
        from pages.incident_card.additional_mode_card_page import AdditionalModeCardPage
        self._return_to_adding_btn.click()
        return AdditionalModeCardPage()

    @allure.step('Нажать кнопку "Продолжить без сохранения"')
    def click_continue_without_saving_button(self):
        from pages.incident_card.saved_accident_сard_page import SavedAccidentCardPage
        self._continue_without_saving_btn.click()
        return SavedAccidentCardPage()
