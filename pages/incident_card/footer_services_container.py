from typing import List

from assertpy import assert_that, soft_assertions
from selene import be, command
from selenium.webdriver.common.keys import Keys

import allure
from selene.api import query

from pages.incident_card.base_container import BaseContainer


class FooterServicesContainer(BaseContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_combinations = [Keys.ALT, 'z']
        self._add_service_btn = self.element.s('//button[@title="Добавить службу"]')
        self._all_services_btn = self.element.s('//button[@title="Все службы"]')
        self._save_card_btn = self.element.s('//button[@title="Все службы"]')
        self._services_titles = self.element.ss('.//div[@class="title"]')
        self._service_button_with_title = lambda service, btn_title: self.element.s(
            f'//span[text()="{service}"]/parent::*/preceding-sibling::*//button[@title="{btn_title}"]')
        self._service_with_status = lambda service, status: self.element.s(
            f'.//div[@class="title"]/parent::div[contains (., "{service}") and  contains(., "{status}")]')

    @allure.step("Клик по кнопке 'Добавить службу'")
    def click_add_service_button(self):
        from pages.incident_card.custom_elements.modal_windows.add_service_modal_window import AddServiceModalWindow
        self._add_service_btn.click()
        return AddServiceModalWindow(xpath='//h1[text()="Добавьте службы"]/parent::div')

    @allure.step("Клик по кнопке 'Все службы'")
    def click_all_services_button(self):
        self._all_services_btn.click()
        return self

    @allure.step("Проверка отсутствия кнопки 'Все службы'")
    def assure_all_services_button_not_visible(self):
        self._all_services_btn.with_(timeout=5).should(be.not_.visible)
        return self

    @allure.step("Удалить службу")
    def delete_service(self, service: dict):
        self._service_button_with_title(service=service['shortTitle'], btn_title='Удалить').with_(timeout=5).click()
        return self

    @allure.step("Проверка отсортированных служб")
    def assure_sorted_services(self, services: List):
        services_titles_ui = [title.get(query.text) for title in self._services_titles]
        sorted_by_id = sorted(services, key=lambda service: service['id'])
        sorted_services = [service['shortTitle'] for service in sorted_by_id]
        assert_that(services_titles_ui).is_equal_to(sorted_services)
        return self

    @allure.step("Проверка отображения служб")
    def assure_footer_services(self, services: List):
        self._services_titles[-1].should(be.visible, timeout=6).perform(command.js.scroll_into_view)
        with soft_assertions():
            services_titles_ui = [title.get(query.text) for title in self._services_titles]
            for service in services:
                service = service['shortTitle'].capitalize() if service['shortTitle'].islower()\
                    else service['shortTitle']
                assert_that(services_titles_ui).contains(service)
        return self

    @allure.step("Проверка статуса у службы")
    def assure_service_status(self, service: str, status: str):
        self._service_with_status(service=service, status=status).should(be.visible, timeout=10)

    @allure.step('Проверка отображения tooltip')
    def assure_edit_service_status_button_tooltip_is_visible(self, service: str):
        self._service_button_with_title(service=service,
                                        btn_title='Выставлен конечный статус').should(be.visible, timeout=5)

    @allure.step('Открытие диалога с изменением статуса службы')
    def open_gos_service_status_dialog(self, service: str):
        from pages.incident_card.custom_elements.modal_windows.gos_service_status_dialog import GosServiceStatusDialog
        self._service_button_with_title(service=service, btn_title='Изменить статус').click()
        return GosServiceStatusDialog(xpath='//md-dialog[contains(@class, "gos-service-status")]')
