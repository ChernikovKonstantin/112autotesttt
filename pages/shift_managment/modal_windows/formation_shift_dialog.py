import allure
from selene import be
from selene.support.shared.jquery_style import s

from pages.common.base_element import BaseElement
from pages.shift_managment.modal_windows.formation_group_dialog import FormationGroupDialog


class FormationShiftDialog(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._formation_group_btn = self.element.s('//button[.="Формирование групп"]')
        self._close_window_btn = self.element.s('.//button[contains (., "закрыть")]')

        s('.loader').with_(timeout=5).should(be.not_.visible)

    @allure.step('Открыть модальное окно "Формирование групп"')
    def open_formation_group_modal_window(self):
        self._formation_group_btn.click()
        return FormationGroupDialog(css='#formationGroup')

    @allure.step('Клик по кнопке закрыть окно')
    def click_close_modal_window_button(self):
        from pages.shift_managment.shift_management_page import ShiftManagementPage
        self._close_window_btn.click()
        return ShiftManagementPage()
