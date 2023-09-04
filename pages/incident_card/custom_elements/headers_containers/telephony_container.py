import allure
from selenium.webdriver.common.keys import Keys

from pages.incident_card.base_container import BaseContainer


class TelephonyContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 'k']
        self._call_records = self.element.s('//button[contains (., "записи звонков")]')
        self._sms_history_list = self.element.s('//button[contains(text() , "список SMS")]')
        self._elements_for_assert = [self._call_records, self._sms_history_list]

    @allure.step('Открыть историю сообщений')
    def open_sms_history_list(self):
        from pages.incident_card.custom_elements.modal_windows.sms_history_window import SmsHistoryDialog
        self._sms_history_list.click()
        return SmsHistoryDialog(css='#smsHistoryDialog')

    @allure.step('Открыть записи разговоров')
    def open_call_records(self):
        from pages.incident_card.custom_elements.modal_windows.record_list_dialog import RecordListDialog
        self._call_records.click()
        return RecordListDialog(css='#recordListDialog')
