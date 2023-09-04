import allure

from data.builders.advanced_search_form_builder import AdvancedSearchFormBuilder
from data.builders.incident_builder import IncidentBuilder
from data.fake_data import TestNames
from data.users.user_list import Users
from utils.pytest_marks import title, tms_link, serial, web_browser


@allure.parent_suite('МЧС')
@allure.suite('Регресс для СТП')
@allure.sub_suite('Управление сменой')
@web_browser
class TestShiftManagement:
    @title('MCHS-2052:(3050)Отображение карточек происшествий операторов смены,'
           ' находящихся под руководством главного спец)')
    @tms_link('MCHS-2052')
    @serial
    def test_mchs_2052(self, login_as, auth_api_client, create_work_shift_group_with_main_specialist_and_users):
        # создание карточек
        incident = IncidentBuilder().with_user_arm(Users.SPECIALIST_1.arm).build()
        incident_id_1 = auth_api_client(user=Users.SPECIALIST_1).create_incident(incident)

        incident = IncidentBuilder().with_user_arm(Users.MASHINISTOV_SPECIALIST.arm).build()
        incident_id_2 = auth_api_client(user=Users.MASHINISTOV_SPECIALIST).create_incident(incident)

        advanced_search_form = AdvancedSearchFormBuilder().with_group_name(TestNames.WORK_SHIFT_GROUP).build()

        with allure.step("Шаги 1-2: Авторизация, поиск по группе и проверка таблицы"):
            for user in [Users.MAIN_SPECIALIST, Users.SHIFT_SUPERVISOR]:
                search_page = login_as(user)
                search_page.close_other_tabs()

                search_page.search_form.open_advanced_form()
                search_page.fill_parameters(advanced_search_form).search_by_parameters_button_click()
                search_page.table.assure_row_contains_value(expected=incident_id_2, row_number=1)
                search_page.table.assure_row_contains_value(expected=incident_id_1, row_number=2)
                search_page.reset_parameters_button_click()

        with allure.step("Шаг 3: Удаление группы"):
            shift_management_page = search_page.head_menu_navigation.go_to_shift_management_page()
            formation_shift_modal_window = shift_management_page.open_formation_shift_modal_window()
            formation_group_modal_window = formation_shift_modal_window.open_formation_group_modal_window()
            delete_group_modal_window = formation_group_modal_window.click_delete_group_with_name(
                group_name=TestNames.WORK_SHIFT_GROUP)
            formation_group_modal_window = delete_group_modal_window.click_button(ok=True)
            formation_shift_modal_window = formation_group_modal_window.click_close_modal_window_button()
            shift_management_page = formation_shift_modal_window.click_close_modal_window_button()

            with allure.step("Проверка удаления группы"):
                search_page = shift_management_page.head_menu_navigation.go_to_search_page()
                search_page.table.wait_loading()
                search_page.assure_parameters_dropdown_options(parameter_dropdown_text='по группе',
                                                               option=TestNames.WORK_SHIFT_GROUP,
                                                               is_visible=False)
