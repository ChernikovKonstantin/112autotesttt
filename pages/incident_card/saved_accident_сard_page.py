import allure

from pages.common_page import BaseAppPage
from pages.incident_card.address_container import AddressContainerSaved
from pages.incident_card.applicant_name_container import ApplicantNameContainerSaved
from pages.incident_card.custom_elements.headers_containers.incident_container import IncidentContainer
from pages.incident_card.custom_elements.headers_containers.phone_containers import AonPhoneContainer, \
    ProvidedContainer, LocationContainer
from pages.incident_card.custom_elements.headers_containers.telephony_container import TelephonyContainer
from pages.incident_card.footer_buttons_container import FooterButtonsContainerSaved
from pages.incident_card.footer_services_container import FooterServicesContainer
from pages.incident_card.incident_description_container import IncidentDescriptionContainerSaved
from pages.incident_card.status_incident_container import StatusIncidentContainer
from pages.incident_card.view_mode_buttons_container import ViewModeButtonsContainer
from pages.incident_card.what_happens_container import WhatHappensContainerSaved
from pages.incident_card.workoff_container import WorkOffContainer


class SavedAccidentCardPage(BaseAppPage):

    def __init__(self):
        super().__init__()
        self.applicant_name_container = ApplicantNameContainerSaved(css='#applicant-name-container div')
        self.aon_phone_container = AonPhoneContainer(css='#aon-container')
        self.provided_phone_container = ProvidedContainer(css='#provided-container')
        self.location_phone_container = LocationContainer(css='#location-container')
        self.telephony_container = TelephonyContainer(css='#telephony-container')
        self.view_mode_buttons_container = ViewModeButtonsContainer(xpath='//*[@class="incident-header__item menu"]')
        self.incident_container = IncidentContainer(css='.incident-container')
        self.address_container = AddressContainerSaved(css='.incident-address__container')
        self.description_container = IncidentDescriptionContainerSaved(
            xpath='//div[contains (@class, "incident-content__description")]')
        self.status_incident_container = StatusIncidentContainer(css="#chs-chp-block")
        self.what_happens = WhatHappensContainerSaved(xpath='//*[contains (@class, "incident-content__what-happened")]')
        self.workoff_container = WorkOffContainer(xpath='//div[contains (@class, "workoff__container")]')
        self.footer_services_container = FooterServicesContainer(css='#footer-services-container')
        self.footer_buttons_container = FooterButtonsContainerSaved(css='.incident-footer-buttons__container')

        self.wait_for_loading()

    @allure.step('Перейти на страницу поиска происшествий')
    def go_to_search_page(self):
        from pages.search_main_page.search_page import SearchPage
        page = SearchPage()
        self.open_page(url=page.url)
        return page
