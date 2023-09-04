import allure
from assertpy import soft_assertions, assert_that
from selene import be

from pages.common.base_element import BaseElement
from pages.incident_card.base_container import BaseContainer


class FooterButtonsContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._save_btn = self.element.s('//button[contains(., "сохранить")]')
        self._card_is_linked_btn = self.element.s('//button[@title="Есть связи"]/span[.="связана"]')

    @allure.step("Клик по кнопке 'Сохранить'")
    def click_save_button(self):
        from pages.incident_card.custom_elements.modal_windows.save_incident_window import SaveIncidentWindow
        self._save_btn.click()
        return SaveIncidentWindow(css='#confirmationSaveIncidentDialog')

    @allure.step("Клик по кнопке 'Сохранить' карточки без описания")
    def click_save_button_card_without_answers(self):
        from pages.incident_card.custom_elements.modal_windows.save_incident_window_without_answers import \
            SaveIncidentWithoutAnswersWindow
        self._save_btn.click()
        return SaveIncidentWithoutAnswersWindow(css='#saveCardWithoutAnswersDialog')

    @allure.step("Проверка наличия кнопки 'Есть связи-связана'")
    def assure_card_linked_button(self):
        self._card_is_linked_btn.should(be.visible)


class FooterButtonsContainerSaved(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._worked_out_btn = self.element.s('//button[normalize-space()="отработана"]')

        self._btn_with_title = lambda title: self.element.s(f'//button[@title="{title}"]')

    @allure.step("Проверка кнопок")
    def assure_buttons(self):
        with soft_assertions():
            self.assure_worked_out_button_is_visible(visible=True)
            for title in ['Создать связь',
                          'Результаты работы отдела контроля',
                          'Будильник',
                          'Важное происшествие',
                          'Сообщить о проблеме',
                          'Закрыть']:
                self.assure_button_with_title_is_visible(button_title=title)
        return self

    @allure.step("Проверка кнопок с тайтлом")
    def assure_button_with_title_is_visible(self, button_title: str):
        assert_that(self._btn_with_title(button_title).matching(be.visible)).is_true()

    @allure.step("Проверка отображения кнопки 'отработана'")
    def assure_worked_out_button_is_visible(self, visible: bool):
        if visible:
            assert_that(self._worked_out_btn.matching(be.visible)).is_true()
        else:
            assert_that(self._worked_out_btn.matching(be.not_.visible)).is_true()

    @allure.step("Клик по кнопке 'Закрыть'")
    def click_close_button(self):
        from pages.search_main_page.search_page import SearchPage
        self._btn_with_title("Закрыть").should(be.clickable, timeout=5).click().should(be.not_.visible, timeout=5)
        return SearchPage()

    @allure.step("Клик по кнопке 'Закрыть' с несохраненной отработкой")
    def click_close_button_with_unsaved_workoff(self):
        from pages.incident_card.custom_elements.modal_windows.close_card_without_save_workoff_window import \
            CloseCardWithoutSaveWorkoffWindow
        self._btn_with_title("Закрыть").should(be.clickable, timeout=5).click()
        return CloseCardWithoutSaveWorkoffWindow(css='#existUnsafeWorkoffWithCloseCard')
