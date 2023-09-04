import allure
from assertpy import soft_assertions, assert_that
from selene import be
from selene.support.shared.jquery_style import s
from selenium.webdriver.common.keys import Keys

from data.buttons import Buttons
from pages.common.base_element import BaseElement


class CloseCardWithoutSaveWorkoffWindow(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ESCAPE]
        self._title = self.element.s('.//h2["Внимание!"]')
        self._first_modal_info = self.element.s('.//div[.="Информация об отработке заполнена, но не сохранена."]')
        self._second_modal_info = self.element.s('.//div[contains (., "Для сохранения отработки нажмите на кнопку")'
                                                 ' and contains (., "справа от заполненной отработки")]')
        self._return_to_workoff_btn = self.element.s(f'.//button[contains (., "{Buttons.RETURN_TO_WORKOFF}")]')
        self._continue_without_saving_btn = self.element.s(
            f'.//button[contains (., "{Buttons.CONTINUE_WITHOUT_SAVING}")]')

        # без прогрузки элемента, окно не закрывается после клика на self._continue_without_saving_btn
        s('//*[@class="md-dialog-backdrop md-opaque"]').should(be.visible, timeout=5)

    @allure.step('Проверка элементов модального окна с инофрмацией о несохраненной отработке')
    def assure_elements_is_visible(self):
        with soft_assertions():
            with allure.step('Проверка заголовка и текстов в окне'):
                assert_that(self._title.matching(be.visible)).is_true()
                assert_that(self._first_modal_info.matching(be.visible)).is_true()
                assert_that(self._second_modal_info.matching(be.visible)).is_true()
            with allure.step('Проверка кнопок'):
                assert_that(self._return_to_workoff_btn.matching(be.visible)).is_true()
                assert_that(self._continue_without_saving_btn.matching(be.visible)).is_true()

    @allure.step('Открытие окна закрытия карточки без сохранения')
    def open_window_by_keyword(self):
        s('//body').press(self._keyboard_combinations)
        return self

    @allure.step('Нажать на кнопку Вернуться к отработке')
    def click_return_to_workoff_button(self):
        from pages.incident_card.saved_accident_сard_page import SavedAccidentCardPage
        self._return_to_workoff_btn.with_(timeout=5).should(be.clickable).click().should(be.hidden)
        return SavedAccidentCardPage()

    @allure.step('Нажать на кнопку Продолжить без сохранения')
    def click_continue_without_saving_button(self):
        from pages.search_main_page.search_page import SearchPage
        self._continue_without_saving_btn.should(be.visible).click()
        return SearchPage()
