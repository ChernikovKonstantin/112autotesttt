from pages.common_page import BaseAppPage
from pages.custom_elements.app_table import GosServicesTabTable


class GosServicesPage(BaseAppPage):

    def __init__(self):
        super().__init__()
        self.table = GosServicesTabTable(xpath='//table[contains (@class, "md-table")]')
