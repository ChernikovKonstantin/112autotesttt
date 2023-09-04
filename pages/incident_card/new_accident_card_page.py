import allure
from assertpy import assert_that
from selene.support.shared.jquery_style import ss
from selenium.webdriver.common.keys import Keys

from data.tooltips import TOOLTIPS
from pages.common_page import BaseAppPage
from pages.incident_card.address_container import AddressContainer
from pages.incident_card.applicant_name_container import ApplicantNameContainer
from pages.incident_card.branch_tags_container import BranchTagsContainer
from pages.incident_card.custom_elements.headers_containers.incident_container import IncidentContainer
from pages.incident_card.custom_elements.headers_containers.phone_containers import (AonPhoneContainer,
                                                                                     ProvidedContainer,
                                                                                     LocationContainer)
from pages.incident_card.custom_elements.headers_containers.telephony_container import TelephonyContainer
from pages.incident_card.custom_elements.headers_containers.timer_container import TimerContainer
from pages.incident_card.custom_elements.modal_windows.accidents_list_window import AccidentsListWindow
from pages.incident_card.custom_elements.modal_windows.alarm_window import NotifyAboutIncidentWindow
from pages.incident_card.custom_elements.modal_windows.close_card_without_save_window import CloseCardWithoutSaveWindow
from pages.incident_card.custom_elements.modal_windows.notify_about_incident_window import ClockAlarmWindow
from pages.incident_card.custom_elements.modal_windows.save_incident_window import SaveIncidentWindow
from pages.incident_card.footer_buttons_container import FooterButtonsContainer
from pages.incident_card.footer_services_container import FooterServicesContainer
from pages.incident_card.incident_description_container import IncidentDescriptionContainer
from pages.incident_card.injured_container import InjuredContainer
from pages.incident_card.reject_container import RejectContainer
from pages.incident_card.question_list_container import QuestionListContainer
from pages.incident_card.what_happens_container import WhatHappensContainer
from pages.incident_card.what_happens_content_branches import FirstBranch, SecondBranch, ThirdBranch
from selene_custom import query

from selene.support.shared import browser
from selenium.webdriver.common.action_chains import ActionChains

from utils.service_utils import wait_seconds


class NewAccidentCardPage(BaseAppPage):

    def __init__(self):
        super().__init__()
        self.applicant_name_container = ApplicantNameContainer(css='#applicant-name-container div')
        self.aon_phone_container = AonPhoneContainer(css='#aon-container')
        self.provided_phone_container = ProvidedContainer(css='#provided-container')
        self.location_phone_container = LocationContainer(css='#location-container')
        self.telephony_container = TelephonyContainer(css='#telephony-container')
        self.incident_container = IncidentContainer(css='.incident-container')
        self.timer_container = TimerContainer(css='.timer-container')
        self.address_container = AddressContainer(css='.incident-address__container')
        self.injured_container = InjuredContainer(css='#injured-container')
        self.reject_container = RejectContainer(css='#reject-btns-container')
        self.what_happens = WhatHappensContainer(css='#what-happened-container')
        self.question_list = QuestionListContainer(css='#question-list-container')
        self.branch_tags = BranchTagsContainer(css='#branch-container')
        self.what_happens_content_branch_1 = FirstBranch(css='#branch-1')
        self.what_happens_content_branch_2 = SecondBranch(css='#branch-2')
        self.what_happens_content_branch_3 = ThirdBranch(css='#branch-3')
        self.description_container = IncidentDescriptionContainer(
            xpath='//div[contains (@class, "incident-content__description")]')
        self.footer_services_container = FooterServicesContainer(css='#footer-services-container')
        self.footer_buttons_container = FooterButtonsContainer(css='.incident-footer-buttons__container')
        self.save_incident_window = SaveIncidentWindow(css='#confirmationSaveIncidentDialog')
        self.clock_alarm_window = ClockAlarmWindow(css='#createClockAlarmMessageDialog')
        self.accidents_list_window = AccidentsListWindow(css='#accidentsListDialog')
        self.notify_about_incident_window = NotifyAboutIncidentWindow(css='#createAlarmMessageDialog')
        self.close_card_without_save_window = CloseCardWithoutSaveWindow(css='#closeCardWithoutSaveDialog')

        self._tooltip = ss('//*[contains (@class, "hotkey-tooltip")]')

        self.wait_for_loading()

    @allure.step('Получение тултипов')
    def get_all_tooltips_ui(self):
        action = ActionChains(browser.driver)
        tooltips_ui = []
        for branch in [self.what_happens_content_branch_1, self.what_happens_content_branch_2]:
            branch.activate_by_keyboard()
            wait_seconds(0.5)
            action.key_down(Keys.ALT).perform()
            tooltips_ui.extend([tooltip.get(query.text) for tooltip in self._tooltip])
            action.reset_actions()
        return tooltips_ui

    @allure.step('Проверить отображение тултипов')
    def assure_tooltips_is_visible(self):
        tooltips_ui = self.get_all_tooltips_ui()
        for tooltip in TOOLTIPS:
            assert_that(tooltips_ui).contains(tooltip)
