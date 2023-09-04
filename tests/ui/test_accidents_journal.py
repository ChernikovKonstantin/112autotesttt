import allure

from api.base_api_112 import BaseApi112
from data.builders.advanced_search_form_builder import AdvancedSearchFormBuilder
from data.builders.incident_builder import IncidentBuilder
from data.gos_services import GosServices
from data.incident_filter_options import OPTIONS_FOR_MAIN_SPECIALIST, OPTIONS_FOR_ORDINARY_SPECIALIST
from data.statuses import IncidentCardStatuses, GosServicesStatuses
from data.users.user_list import Users
from utils.pytest_marks import title, tms_link, serial, web_browser


@allure.parent_suite('МЧС')
@allure.suite('Регресс для СТП')
@allure.sub_suite('Журнал происшествий')
@web_browser
class TestAccidentsJournal:

    @title('MCHS-1152: Фильтр происшествий "выберите,что показывать" (главный специалист)')
    @tms_link('MCHS-1152')
    @serial
    def test_mchs_1152(self, login_as, auth_api_client):
        # создание карточки в статусе Черновик
        spec_1_auth_api_client = auth_api_client(user=Users.SPECIALIST_1)
        status_draft_incident_id = spec_1_auth_api_client.get_new_incident_number(work_place=Users.SPECIALIST_1.arm)

        # отправка карточки из внешней системы
        incident_from_external_service_id = BaseApi112().send_new_card_from_external_service()

        # создание связанной карточки с пострадавшими
        main_spec_auth_api_client = auth_api_client(user=Users.MAIN_SPECIALIST)
        parent_incident = IncidentBuilder().with_user_arm(Users.MAIN_SPECIALIST.arm).build()
        parent_incident_id = main_spec_auth_api_client.create_incident(parent_incident)
        incident_with_injured = IncidentBuilder() \
            .with_user_arm(Users.MAIN_SPECIALIST.arm) \
            .with_injured_count('2') \
            .build()
        incident_with_injured_id = main_spec_auth_api_client.create_incident(incident_with_injured)
        main_spec_auth_api_client.bind_cards(parent_incident_id=parent_incident_id,
                                             incident_id=incident_with_injured_id)

        with allure.step("Шаг 1: Авторизация и проверка фильтров в дропдауне"):
            search_page = login_as(Users.MAIN_SPECIALIST)
            search_page.close_other_tabs()
            search_page.cards_filter_dropdown.assure_values('выберите что показывать')
            search_page.cards_filter_dropdown.click()
            search_page.assure_filter_options(options=OPTIONS_FOR_MAIN_SPECIALIST)
        with allure.step("Шаг 2: Проверка сворачивания дропдауна"):
            search_page.cards_filter_dropdown.click().options_is(visible=True)
            search_page.catcher_click().table.wait_loading()
            search_page.cards_filter_dropdown.options_is(visible=False)
        with allure.step("Шаг 3: Проверка фильтра 'Несохраненные карточки'"):
            search_page.cards_filter_dropdown.choose_values('несохраненные карточки')
            search_page.catcher_click().table.wait_loading()
            search_page.table.assure_row_contains_value(expected=status_draft_incident_id, row_number=1)
            search_page.cards_filter_dropdown.deselect()
            search_page.catcher_click().table.wait_loading()
        with allure.step("Шаг 4: Проверка фильтров 'Связанные карточки', 'Где есть пострадавшие'"):
            search_page.cards_filter_dropdown.choose_values('связанные карточки', 'где есть пострадавшие')
            search_page.catcher_click().table.wait_loading()
            search_page.table.assure_row_contains_value(expected=incident_with_injured_id, row_number=1)
            search_page.cards_filter_dropdown.deselect()
            search_page.catcher_click().table.wait_loading()
        with allure.step("Шаг 5: Проверка фильтра 'Карточка в очереди'"):
            search_page.cards_filter_dropdown.choose_values('карточки в очереди')
            search_page.catcher_click().table.wait_loading()
            search_page.table.assure_row_contains_value(expected=incident_from_external_service_id, row_number=1)
            search_page.cards_filter_dropdown.deselect()
            search_page.catcher_click().table.wait_loading()
        with allure.step("Шаг 6: Проверка фильтра 'Непроверенные карточки'"):
            search_page.cards_filter_dropdown.choose_values('непроверенные карточки')
            search_page.catcher_click().table.wait_loading()
            search_page.table.assure_row_contains_value(expected=incident_with_injured_id, row_number=1)
            search_page.cards_filter_dropdown.deselect()
            search_page.catcher_click().table.wait_loading()
        with allure.step("Шаг 7: Проверка фильтра 'Система 112'"):
            search_page.cards_filter_dropdown.choose_values('Система 112')
            search_page.catcher_click().table.wait_loading()
            search_page.table.assure_row_contains_value(expected=incident_with_injured_id, row_number=1)
            search_page.table.assure_row_contains_value(expected=parent_incident_id, row_number=2)

    @title('MCHS-2113: Фильтр происшествий (специалист)')
    @tms_link('MCHS-2113')
    @serial
    def test_mchs_2113(self, login_as, auth_api_client):
        # создание карточки в статусе Черновик
        spec_1_auth_api_client = auth_api_client(user=Users.SPECIALIST_1)
        status_draft_incident_id = spec_1_auth_api_client.get_new_incident_number(work_place=Users.SPECIALIST_1.arm)

        # создание связанной карточки с пострадавшими
        main_spec_auth_api_client = auth_api_client(user=Users.MAIN_SPECIALIST)
        parent_incident = IncidentBuilder().with_user_arm(Users.MAIN_SPECIALIST.arm).build()
        parent_incident_id = main_spec_auth_api_client.create_incident(parent_incident)
        incident_with_injured = IncidentBuilder() \
            .with_user_arm(Users.MAIN_SPECIALIST.arm) \
            .with_injured_count('2') \
            .build()
        incident_with_injured_id = main_spec_auth_api_client.create_incident(incident_with_injured)
        main_spec_auth_api_client.bind_cards(parent_incident_id=parent_incident_id,
                                             incident_id=incident_with_injured_id)

        advanced_search_form = AdvancedSearchFormBuilder() \
            .with_user_arm(Users.MAIN_SPECIALIST.arm) \
            .with_status(IncidentCardStatuses.REGISTERED.title) \
            .with_incident_id(incident_with_injured_id) \
            .build()

        with allure.step("Шаг 1: Авторизация и проверка фильтров в дропдауне"):
            search_page = login_as(Users.SPECIALIST_1)
            search_page.close_other_tabs()
            search_page.cards_filter_dropdown.assure_values('выберите что показывать')
            search_page.cards_filter_dropdown.click()
            search_page.assure_filter_options(options=OPTIONS_FOR_ORDINARY_SPECIALIST)
        with allure.step("Шаг 2: Проверка сворачивания дропдауна"):
            search_page.cards_filter_dropdown.click().options_is(visible=True)
            search_page.catcher_click().table.wait_loading()
            search_page.cards_filter_dropdown.options_is(visible=False)
        with allure.step("Шаг 3: Проверка фильтра 'Несохраненные карточки'"):
            search_page.cards_filter_dropdown.choose_values('несохраненные карточки')
            search_page.catcher_click().table.wait_loading()
            search_page.table.assure_row_contains_value(expected=status_draft_incident_id, row_number=1)
            search_page.cards_filter_dropdown.deselect()
            search_page.catcher_click().table.wait_loading()
        with allure.step("Шаг 4: Проверка фильтров 'Связанные карточки', 'Где есть пострадавшие', "
                         "'карточки других операторов'"):
            search_page.cards_filter_dropdown.choose_values('связанные карточки',
                                                            'где есть пострадавшие',
                                                            'карточки других операторов')
            search_page.catcher_click().table.wait_loading()
            search_page.table.assure_row_contains_value(expected=incident_with_injured_id, row_number=1)
        with allure.step("Шаг 5: Проверка дополнительной фильтрации"):
            search_page.cards_filter_dropdown.choose_values('создана вручную', 'Система 112')
            search_page.catcher_click().table.wait_loading()
            search_page.table.assure_row_contains_value(expected=incident_with_injured_id, row_number=1)
        with allure.step("Шаг 6: Выбор и поиск по параметрам"):
            search_page.search_form.open_advanced_form()
            search_page.fill_parameters(advanced_search_form).search_by_parameters_button_click()
            search_page.table.assure_row_contains_value(expected=incident_with_injured_id, row_number=1)
            search_page.reset_parameters_button_click()
            search_page.cards_filter_dropdown.assure_values('связанные карточки',
                                                            'где есть пострадавшие',
                                                            'карточки других операторов',
                                                            'создана вручную',
                                                            'Система 112')

    @title('MCHS-1884: Проставление статусов реагирования')
    @tms_link('MCHS-1884')
    @serial
    def test_mchs_1884(self, login_as, auth_api_client):
        with allure.step("Шаг 0: Создание карточки со службой ФСБ и авторизация"):
            incident_with_fsb_service = IncidentBuilder() \
                .with_user_arm(Users.SPECIALIST_1.arm) \
                .with_gos_service_id(GosServices.SERVICE_FSB.id) \
                .build()
            spec_1_auth_api_client = auth_api_client(user=Users.SPECIALIST_1)
            incident_with_fsb_service_id = spec_1_auth_api_client.create_incident(incident_with_fsb_service)
            search_page = login_as(Users.FSB_SPECIALIST)
            search_page.close_other_tabs()
        with allure.step("Шаг 1-3: Выбор и проверка статуса Получена службой"):
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.ADDED, row_number=1)
            change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                incident_id=incident_with_fsb_service_id)
            change_status_modal_window.assure_allowed_statuses(GosServicesStatuses.RECEIVED)
            change_status_modal_window.choose_status(GosServicesStatuses.RECEIVED)
            search_page = change_status_modal_window.save_and_close()
            search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.RECEIVED, row_number=1)
        with allure.step("Шаг 4-5: Проверка статусов и выбор статуса Принята"):
            change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                incident_id=incident_with_fsb_service_id)
            change_status_modal_window.assure_allowed_statuses(GosServicesStatuses.ACCEPTED,
                                                               GosServicesStatuses.NOT_ACCEPTED)
            change_status_modal_window.choose_status(GosServicesStatuses.ACCEPTED)
            search_page = change_status_modal_window.save_and_close()
            search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.ACCEPTED, row_number=1)
        with allure.step("Шаг 6-7: Проверка статусов и выбор статуса Начало реагирования"):
            change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                incident_id=incident_with_fsb_service_id)
            change_status_modal_window.assure_allowed_statuses(GosServicesStatuses.START_RESPONSE,
                                                               GosServicesStatuses.CANCEL_PERFORM_WORKS,
                                                               GosServicesStatuses.WORKS_FINISHED)
            change_status_modal_window.choose_status(GosServicesStatuses.START_RESPONSE)
            search_page = change_status_modal_window.save_and_close()
            search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.START_RESPONSE, row_number=1)
        with allure.step("Шаг 8-9: Проверка статусов и выбор статуса Прибытие"):
            change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                incident_id=incident_with_fsb_service_id)
            change_status_modal_window.assure_allowed_statuses(GosServicesStatuses.ARRIVED,
                                                               GosServicesStatuses.CANCEL_PERFORM_WORKS,
                                                               GosServicesStatuses.WORKS_FINISHED)
            change_status_modal_window.choose_status(GosServicesStatuses.ARRIVED)
            search_page = change_status_modal_window.save_and_close()
            search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.ARRIVED, row_number=1)
        with allure.step("Шаг 10-11: Проверка статусов и выбор статуса Проведение работ"):
            change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                incident_id=incident_with_fsb_service_id)
            change_status_modal_window.assure_allowed_statuses(GosServicesStatuses.EXECUTION_WORKS,
                                                               GosServicesStatuses.CANCEL_PERFORM_WORKS,
                                                               GosServicesStatuses.WORKS_FINISHED)
            change_status_modal_window.choose_status(GosServicesStatuses.EXECUTION_WORKS)
            search_page = change_status_modal_window.save_and_close()
            search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.EXECUTION_WORKS, row_number=1)
        with allure.step("Шаг 12-13: Проверка статусов, блокировки кнопки, выбор статуса Работы завершены"):
            change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                incident_id=incident_with_fsb_service_id)
            change_status_modal_window.assure_allowed_statuses(GosServicesStatuses.CANCEL_PERFORM_WORKS,
                                                               GosServicesStatuses.WORKS_FINISHED)
            change_status_modal_window.choose_status(GosServicesStatuses.WORKS_FINISHED)
            search_page = change_status_modal_window.save_and_close()
            search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.WORKS_FINISHED, row_number=1)
            search_page.table.assure_final_status_tooltip_for_incident_is_visible(
                incident_id=incident_with_fsb_service_id)

    @title('MCHS-2114: Проставление статусов реагирования: комбинации статусов')
    @tms_link('MCHS-2114')
    @serial
    def test_mchs_2114(self, login_as, auth_api_client):
        with allure.step("Шаг 0: Создание карточек со службой ФСБ и авторизация"):
            incident_with_fsb_service = IncidentBuilder() \
                .with_user_arm(Users.SPECIALIST_1.arm) \
                .with_gos_service_id(GosServices.SERVICE_FSB.id) \
                .build()
            spec_1_auth_api_client = auth_api_client(user=Users.SPECIALIST_1)
            incident_with_fsb_service_id_1 = spec_1_auth_api_client.create_incident(incident_with_fsb_service)
            incident_with_fsb_service_id_2 = spec_1_auth_api_client.create_incident(incident_with_fsb_service)
            incident_with_fsb_service_id_3 = spec_1_auth_api_client.create_incident(incident_with_fsb_service)
            incident_with_fsb_service_id_4 = spec_1_auth_api_client.create_incident(incident_with_fsb_service)
            incident_with_fsb_service_id_5 = spec_1_auth_api_client.create_incident(incident_with_fsb_service)
            search_page = login_as(Users.FSB_SPECIALIST)
            search_page.close_other_tabs()

        with allure.step("Шаг 1: Выбор и проверка конечного статуса для первой карточки"):
            for status in [GosServicesStatuses.RECEIVED,
                           GosServicesStatuses.ACCEPTED,
                           GosServicesStatuses.START_RESPONSE,
                           GosServicesStatuses.ARRIVED,
                           GosServicesStatuses.EXECUTION_WORKS,
                           GosServicesStatuses.CANCEL_PERFORM_WORKS,
                           ]:
                change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                    incident_id=incident_with_fsb_service_id_1)
                change_status_modal_window.choose_status(status)
                search_page = change_status_modal_window.save_and_close()
                search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.CANCEL_PERFORM_WORKS,
                                                        row_number=5)
            search_page.table.assure_final_status_tooltip_for_incident_is_visible(
                incident_id=incident_with_fsb_service_id_1)
            card_page = search_page.go_to_incident_page(incident_id=incident_with_fsb_service_id_1)
            card_page.footer_services_container.assure_service_status(service=GosServices.SERVICE_FSB.title,
                                                                      status=GosServicesStatuses.CANCEL_PERFORM_WORKS)
            card_page.footer_services_container.assure_edit_service_status_button_tooltip_is_visible(
                service=GosServices.SERVICE_FSB.title)
            search_page = card_page.go_to_search_page()
            search_page.table.wait_loading()

        with allure.step("Шаг 2: Выбор и проверка конечного статуса для второй карточки"):
            for status in [GosServicesStatuses.RECEIVED,
                           GosServicesStatuses.ACCEPTED,
                           GosServicesStatuses.WORKS_FINISHED,
                           ]:
                change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                    incident_id=incident_with_fsb_service_id_2)
                change_status_modal_window.choose_status(status)
                search_page = change_status_modal_window.save_and_close()
                search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.WORKS_FINISHED,
                                                        row_number=4)
            search_page.table.assure_final_status_tooltip_for_incident_is_visible(
                incident_id=incident_with_fsb_service_id_2)
            card_page = search_page.go_to_incident_page(incident_id=incident_with_fsb_service_id_2)
            card_page.footer_services_container.assure_service_status(service=GosServices.SERVICE_FSB.title,
                                                                      status=GosServicesStatuses.WORKS_FINISHED)
            card_page.footer_services_container.assure_edit_service_status_button_tooltip_is_visible(
                service=GosServices.SERVICE_FSB.title)
            search_page = card_page.go_to_search_page()
            search_page.table.wait_loading()

        with allure.step("Шаг 3: Выбор и проверка конечного статуса для третьей карточки"):
            for status in [GosServicesStatuses.RECEIVED,
                           GosServicesStatuses.ACCEPTED,
                           GosServicesStatuses.START_RESPONSE,
                           GosServicesStatuses.WORKS_FINISHED,
                           ]:
                change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                    incident_id=incident_with_fsb_service_id_3)
                change_status_modal_window.choose_status(status)
                search_page = change_status_modal_window.save_and_close()
                search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.WORKS_FINISHED,
                                                        row_number=3)
            search_page.table.assure_final_status_tooltip_for_incident_is_visible(
                incident_id=incident_with_fsb_service_id_3)
            card_page = search_page.go_to_incident_page(incident_id=incident_with_fsb_service_id_3)
            card_page.footer_services_container.assure_service_status(service=GosServices.SERVICE_FSB.title,
                                                                      status=GosServicesStatuses.WORKS_FINISHED)
            card_page.footer_services_container.assure_edit_service_status_button_tooltip_is_visible(
                service=GosServices.SERVICE_FSB.title)
            search_page = card_page.go_to_search_page()
            search_page.table.wait_loading()

        with allure.step("Шаг 4: Выбор и проверка конечного статуса для четвертой карточки"):
            for status in [GosServicesStatuses.RECEIVED,
                           GosServicesStatuses.ACCEPTED,
                           GosServicesStatuses.START_RESPONSE,
                           GosServicesStatuses.WORKS_FINISHED,
                           ]:
                change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                    incident_id=incident_with_fsb_service_id_4)
                change_status_modal_window.choose_status(status)
                search_page = change_status_modal_window.save_and_close()
                search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.WORKS_FINISHED,
                                                        row_number=2)
            search_page.table.assure_final_status_tooltip_for_incident_is_visible(
                incident_id=incident_with_fsb_service_id_4)
            card_page = search_page.go_to_incident_page(incident_id=incident_with_fsb_service_id_4)
            card_page.footer_services_container.assure_service_status(service=GosServices.SERVICE_FSB.title,
                                                                      status=GosServicesStatuses.WORKS_FINISHED)
            card_page.footer_services_container.assure_edit_service_status_button_tooltip_is_visible(
                service=GosServices.SERVICE_FSB.title)
            search_page = card_page.go_to_search_page()
            search_page.table.wait_loading()

        with allure.step("Шаг 5: Выбор и проверка конечного статуса для пятой карточки"):
            for status in [GosServicesStatuses.RECEIVED,
                           GosServicesStatuses.NOT_ACCEPTED
                           ]:
                change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                    incident_id=incident_with_fsb_service_id_5)
                change_status_modal_window.choose_status(status)
                search_page = change_status_modal_window.save_and_close()
                search_page.table.wait_loading()
            search_page.table.assure_row_contains_value(expected=GosServicesStatuses.NOT_ACCEPTED, row_number=1)
            change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                incident_id=incident_with_fsb_service_id_5)
            change_status_modal_window.assure_allowed_statuses(GosServicesStatuses.ACCEPTED)

