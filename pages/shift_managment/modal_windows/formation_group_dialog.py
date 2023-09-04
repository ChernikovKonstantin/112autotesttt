import allure
from selene import be

from pages.common.base_element import BaseElement


class FormationGroupDialog(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._delete_group_btn = lambda group_name: self.element.s(
            f'.//span[contains (@title, "{group_name}")]'
            f'/ancestor::div[contains (@class, "grid-body")]//i[contains (., "delete")]')
        self._close_window_btn = self.element.s('.//button[contains (., "закрыть")]')

    @allure.step('Клик по кнопке удаления группы с именем')
    def click_delete_group_with_name(self, group_name):
        from pages.shift_managment.modal_windows.delete_group_dialog import DeleteGroupDialog
        self._delete_group_btn(group_name).with_(timeout=5).should(be.clickable).click()
        return DeleteGroupDialog(xpath='//h2[.="Удаление группы"]/ancestor::md-dialog')

    @allure.step('Клик по кнопке закрыть окно')
    def click_close_modal_window_button(self):
        from pages.shift_managment.shift_management_page import FormationShiftDialog
        self._close_window_btn.click()
        return FormationShiftDialog(xpath='//md-dialog[contains(@class, "shift-formation")]')
