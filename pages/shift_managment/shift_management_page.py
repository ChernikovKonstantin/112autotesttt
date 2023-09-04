import allure
from selene.support.shared.jquery_style import s

from pages.common_page import BaseAppPage
from pages.custom_elements.head_menu_navigation import HeadMenuNavigation
from pages.shift_managment.modal_windows.formation_shift_dialog import FormationShiftDialog


class ShiftManagementPage(BaseAppPage):

    def __init__(self):
        super().__init__()
        self._formation_shift_btn = s('//button[.="Формирование смены"]')
        self.head_menu_navigation = HeadMenuNavigation(css='.head-menu__navigation')

        self.wait_for_loading()

    @allure.step('Открыть модальное окно "Формирование смены"')
    def open_formation_shift_modal_window(self):
        self._formation_shift_btn.click()
        return FormationShiftDialog(xpath='//md-dialog[contains(@class, "shift-formation")]')