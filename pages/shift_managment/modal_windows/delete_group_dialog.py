import allure

from pages.common.base_element import BaseElement
from pages.shift_managment.modal_windows.formation_group_dialog import FormationGroupDialog
from utils.service_utils import wait_seconds


class DeleteGroupDialog(BaseElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ok_btn = self.element.s('.//button[.="ОК"]')
        self._cancel_btn = self.element.s('.//button[.="Отмена"]')

        self.waiting_to_be_visible(timeout=10)

    @allure.step('Клик по кнопке OK/Отмена')
    def click_button(self, ok=False, cancel=False):
        wait_seconds(0.6)  # костыль, тк без таймаута происходит закрытие предыдущего модального окна
        if ok:
            self._ok_btn.click()
        elif cancel:
            self._cancel_btn.click()
        return FormationGroupDialog(xpath='//md-dialog[contains(@aria-label, "Формирование групп")]')
