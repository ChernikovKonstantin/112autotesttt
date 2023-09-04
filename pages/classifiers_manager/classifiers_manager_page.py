import allure
from selene.support.shared.jquery_style import s

from data.gos_services import GosService
from pages.common_page import BaseAppPage
from pages.classifiers_manager.gos_services_page import GosServicesPage
from pages.classifiers_manager.polygon_reaction_page import PolygonReactionPage
from pages.custom_elements.app_table import ClassifiersManagerTabTable


class ClassifiersManagerPage(BaseAppPage):

    def __init__(self):
        super().__init__()
        self._tabs = lambda tab_name: s(f'//a[.="{tab_name}"]')
        self.table = ClassifiersManagerTabTable(xpath='//table[contains (@class, "md-table")]')

        self.wait_for_loading()

    @allure.step('Открыть вкладку "Полигоны реагирования"')
    def open_polygon_reaction_tab(self):
        self._tabs(tab_name='Полигоны реагирования').click()
        return PolygonReactionPage()

    @allure.step('Открыть вкладку "Справочник служб"')
    def open_gos_services_tab(self):
        self._tabs(tab_name='Справочник служб').click()
        return GosServicesPage()

    @allure.step('Добавление службы в классификатор')
    def add_gos_service_to_classifier(self, classifier: str, gos_service: GosService, service_condition: str):
        self.table.click_edit_button_in_row_contains_text(classifier)
        self.table.click_add_service_button()
        self.table.edit_classifier(gos_service=gos_service.title, service_condition=service_condition)
        self.table.click_save_button_in_row_contains_text(gos_service.title)
        return self
