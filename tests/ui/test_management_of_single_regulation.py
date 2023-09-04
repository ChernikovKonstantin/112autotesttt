import allure

from data.fake_data import faker
from data.gos_services import GosServices
from data.users.user_list import Users
from database import mchs_112_db_connect
from utils.pytest_marks import title, tms_link, serial, web_browser


@allure.parent_suite('МЧС')
@allure.suite('Регресс для СТП')
@allure.sub_suite('Управление единым регламентом')
@web_browser
class TestManagementOfSingleRegulation:

    @title('MCHS-2030: (2999)Поиск службы по наименованию в списке выбора служб для привязки геосегмента к службе')
    @tms_link('MCHS-2030')
    def test_mchs_2030(self, login_as, delete_test_polygons_after_test):
        with allure.step('Подготовка тестовых данных'):
            polygon_name = f'{faker().city()}_автотест'
            delete_test_polygons_after_test(polygon_name)

            search_page = login_as(Users.MAIN_SPECIALIST)
            search_page.close_other_tabs()
            classifiers_manager_page = search_page.head_menu_navigation.go_to_classifiers_manager_page()
            classifiers_manager_page.close_other_tabs()
            polygon_reaction_tab = classifiers_manager_page.open_polygon_reaction_tab()
            polygon_reaction_tab.close_other_tabs()
            polygon_reaction_tab.add_polygon(name=polygon_name)
        with allure.step('Шаг 1-2: Поиск и редактирование службы 101'):
            gos_services_tab = classifiers_manager_page.open_gos_services_tab()
            gos_services_tab.close_other_tabs()
            search_page.search_form.set_value_and_search(value=GosServices.SERVICE_101.title)
            gos_services_tab.table.assure_row_contains_value(expected=GosServices.SERVICE_101.title, row_number=1)
            gos_services_tab.table.click_edit_button_in_row_contains_text(row_text=GosServices.SERVICE_101.title)
            gos_services_tab.close_other_tabs()
        with allure.step('Шаг 3: Добавление полигона в район выезда'):
            gos_services_tab.table.add_district(name=polygon_name)
            search_page.catcher_click()
            gos_services_tab.table.click_save_button_in_row_contains_text(row_text=GosServices.SERVICE_101.title)
        with allure.step('Шаг 4: Проверка отображения геосегментов'):
            gos_services_tab.table.assure_districts_have_tooltip(tooltip=polygon_name)
        with allure.step('Шаг 5: Проверка привязки полигона к службе'):
            gos_service = mchs_112_db_connect.get_gos_service_by_polygon_name(polygon_name=polygon_name)[1]
            assert 'Служба 101' == gos_service
