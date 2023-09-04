import allure

from data.builders.address_builder import AddressBuilder
from data.dates import get_current_date
from data.fake_data import faker
from data.gos_services import GosServices
from data.polygon_coordinates import PolygonCoordinates
from data.users.user_list import Users
from data.what_happens_incident_contents import INCIDENTS
from database import mchs_112_db_connect
from utils.common_check import assure_that_values_in_text
from utils.pytest_marks import title, tms_link, web_browser


@allure.parent_suite('МЧС')
@allure.suite('Регресс для СТП')
@allure.sub_suite('Полигоны реагирования ')
@web_browser
class TestPolygonReaction:
    @title('MCHS-2118: (2989) Логирование изменений геосегментов экстренных оперативных'
           'и аварийно-восстановительных служб')
    @tms_link('MCHS-2118')
    def test_mchs_2118(self, login_as, delete_test_polygons_after_test):
        with allure.step('Создание тестовых данных и инициализация фикстуры'):
            polygon_name = f'{faker().city()}_автотест'
            new_polygon_name = f'{faker().city()}_автотест'
            draft_polygon_name = f'{faker().city()}_автотест'

            delete_test_polygons_after_test(polygon_name, new_polygon_name, draft_polygon_name)

        with allure.step('Шаги 1-2: Авторизация - Переход на вкладку УЕР - Добавление полигона'):
            search_page = login_as(Users.MAIN_SPECIALIST)
            search_page.close_other_tabs()
            classifiers_manager_page = search_page.head_menu_navigation.go_to_classifiers_manager_page()
            classifiers_manager_page.close_other_tabs()
            polygon_reaction_tab = classifiers_manager_page.open_polygon_reaction_tab()
            polygon_reaction_tab.close_other_tabs()
            polygon_reaction_tab.add_polygon(name=polygon_name)
        with allure.step('Шаг 3: Проверка кнопок'):
            polygon_reaction_tab.assure_buttons(polygon_name=polygon_name)

        with allure.step('Шаг 4: Редактирование/обновление полигона'):
            polygon_reaction_tab.click_edit_button_polygon_with_name(name=polygon_name)
            polygon_reaction_tab.click_edit_mode_polygon_button_with_text(text='Обновить полигон')
            polygon_reaction_tab.assure_color_update_polygon_button()
            polygon_reaction_tab.delete_dot_on_map()
            polygon_reaction_tab.add_polygon_dot()
            polygon_reaction_tab.set_polygon_name(name=new_polygon_name)
            polygon_reaction_tab.click_edit_mode_polygon_button_with_text(text='Сохранить')

        with allure.step('Шаги 5-6: Проверка сохранения/обновления данных полигона в БД'):
            polygon_coords_from_db = mchs_112_db_connect.get_polygon_coords_by_name(polygon_name=new_polygon_name)
            assure_that_values_in_text(polygon_coords_from_db[0][0], *PolygonCoordinates.POLYGON_DISTRICT_COORD)

            old_polygon_history_coords_from_db = mchs_112_db_connect.get_value_from_polygon_history_by_old_name(
                value='st_astext(old_polygon_coordinate)', polygon_name=polygon_name)
            assure_that_values_in_text(old_polygon_history_coords_from_db[0][0], *PolygonCoordinates.HISTORY_OLD_COORD)

            new_polygon_history_coords_from_db = mchs_112_db_connect.get_value_from_polygon_history_by_old_name(
                value='st_astext(new_polygon_coordinate)', polygon_name=polygon_name)
            assure_that_values_in_text(new_polygon_history_coords_from_db[0][0], *PolygonCoordinates.HISTORY_NEW_COORD)

            old_polygon_history_name_from_db = mchs_112_db_connect.get_value_from_polygon_history_by_old_name(
                value='old_polygon_name', polygon_name=polygon_name)
            assure_that_values_in_text(old_polygon_history_name_from_db[0][0], polygon_name)

            new_polygon_history_name_from_db = mchs_112_db_connect.get_value_from_polygon_history_by_old_name(
                value='new_polygon_name', polygon_name=polygon_name)
            assure_that_values_in_text(new_polygon_history_name_from_db[0][0], new_polygon_name)

            date_from_db = mchs_112_db_connect.get_value_from_polygon_history_by_old_name(
                value='changed_date', polygon_name=polygon_name)
            assure_that_values_in_text(str(date_from_db[0][0]), get_current_date(format_string='%y-%m-%d'))

            employee_id_from_db = mchs_112_db_connect.get_value_from_polygon_history_by_old_name(
                value='employee_id', polygon_name=polygon_name)
            assure_that_values_in_text(str(employee_id_from_db[0][0]), str(Users.MAIN_SPECIALIST.id))

            event_type_from_db = mchs_112_db_connect.get_value_from_polygon_history_by_old_name(
                value='event_type', polygon_name=polygon_name)
            assure_that_values_in_text(str(event_type_from_db[0][0]), '1')

        with allure.step('Шаги 7-8: Проверка отмены редактирования полигона'):
            polygon_reaction_tab.click_edit_button_polygon_with_name(name=new_polygon_name)
            polygon_reaction_tab.set_polygon_name(name=draft_polygon_name)
            polygon_reaction_tab.click_edit_mode_polygon_button_with_text(text='Отмена редактирования')

            new_polygon_history_name_from_db = mchs_112_db_connect.get_value_from_polygon_history_by_old_name(
                value='new_polygon_name', polygon_name=polygon_name)
            assure_that_values_in_text(new_polygon_history_name_from_db[0][0], new_polygon_name)

        with allure.step('Шаги 9-10: Удаление полигона и проверка в БД'):
            polygon_reaction_tab.click_edit_button_polygon_with_name(name=new_polygon_name)
            polygon_reaction_tab.click_edit_mode_polygon_button_with_text(text='Удалить полигон')
            polygon_coords_from_db = mchs_112_db_connect.get_polygon_coords_by_name(polygon_name=new_polygon_name)
            assert polygon_coords_from_db is None

    @title('MCHS-1974: (2981) Реализация механизма предоставления доступа к электронным формам отображения набора граф')
    @tms_link('MCHS-1974')
    def test_mchs_1974(self, login_as, add_test_gos_service, delete_test_polygons_after_test):
        with allure.step('Создание тестовых данных и инициализация фикстуры'):
            polygon_name = f'{faker().city()}_автотест'
            delete_test_polygons_after_test(polygon_name)

            suggest_address = AddressBuilder() \
                .with_street('Театральная площадь') \
                .with_house_number('5') \
                .with_housing('3') \
                .build()

        with allure.step('Шаг 1: Авторизация - Переход на вкладку УЕР - Добавление службы для типа пожар: мусор'):
            search_page = login_as(Users.MAIN_SPECIALIST)
            search_page.close_other_tabs()

            classifiers_manager_page = search_page.head_menu_navigation.go_to_classifiers_manager_page()
            classifiers_manager_page.close_other_tabs()
            classifiers_manager_page.add_gos_service_to_classifier(classifier='пожар: мусор',
                                                                   gos_service=GosServices.AUTO_TEST_SERVICE,
                                                                   service_condition='выезд всегда')

        with allure.step('Шаг 2: Создание полигона - Проверка сообщения о запрете удаления привязанного полигона'):
            polygon_reaction_tab = classifiers_manager_page.open_polygon_reaction_tab()
            polygon_reaction_tab.close_other_tabs()
            polygon_reaction_tab.add_polygon(name=polygon_name, polygon_with_building=True)

            gos_services_tab = classifiers_manager_page.open_gos_services_tab()
            gos_services_tab.close_other_tabs()
            gos_services_tab.table.click_edit_button_in_row_contains_text(row_text=GosServices.AUTO_TEST_SERVICE.title)
            gos_services_tab.close_other_tabs()
            gos_services_tab.table.add_district(name=polygon_name)
            gos_services_tab.catcher_click()
            gos_services_tab.table.click_save_button_in_row_contains_text(row_text=GosServices.AUTO_TEST_SERVICE.title)

            polygon_reaction_tab = classifiers_manager_page.open_polygon_reaction_tab()
            polygon_reaction_tab.click_edit_button_polygon_with_name(name=polygon_name)
            polygon_reaction_tab.close_other_tabs()
            cant_delete_polygon_modal_window = polygon_reaction_tab.click_delete_binding_polygon_button_with_text()
            cant_delete_polygon_modal_window.assert_message_text()
            polygon_reaction_tab = cant_delete_polygon_modal_window.click_ok_button()

        with allure.step('Шаг 3: Проверка подгрузки службы в карточку по адресу из полигона'):
            new_card_page = polygon_reaction_tab.go_to_new_card_page_by_keyboard()
            new_card_page.close_other_tabs()
            new_card_page.address_container.set_values_to_input_fields(address=suggest_address)

            # повторное заполнение формы, тк Строение в адресе при первом заполнении периодически сбрасывается
            new_card_page.close_other_tabs()
            new_card_page.address_container.set_values_to_input_fields(address=suggest_address)

            new_card_page.what_happens.activate_by_keyboard()
            new_card_page.what_happens.choose_incident_tag(tag_name=INCIDENTS['101'].name)
            new_card_page.what_happens_content_branch_1.choose_answers(INCIDENTS['101'].answers)
            new_card_page.wait_for_loading()
            new_card_page.footer_services_container.assure_footer_services(
                services=[{'shortTitle': GosServices.AUTO_TEST_SERVICE.title}])
