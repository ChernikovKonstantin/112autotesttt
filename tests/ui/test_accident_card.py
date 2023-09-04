import allure
import pytest

from data.builders.address_builder import AddressBuilder
from data.builders.applicant_name_builder import ApplicantNameBuilder
from data.builders.incident_builder import IncidentBuilder
from data.builders.record_call_builder import RecordCallBuilder
from data.builders.sms_history_builder import SmsHistoryBuilder
from data.builders.workoff_builder import WorkoffFormBuilder
from data.dates import get_current_date
from data.gos_services import GosServices
from data.phone_numbers import PhoneNumbers
from data.statuses import SmsStatuses, IncidentCardStatuses, GosServicesStatuses
from data.suggestions import LOCATION_BY_AON_NUMBER
from data.users.user_list import Users
from data.what_happens_incident_contents import INCIDENTS
from database import mchs_112_db_connect
from utils.pytest_marks import web_browser, tms_link, title, serial, data_provider
from utils.service_utils import random_choice_items_from_list, get_random_number_with_digits_len


@allure.parent_suite('МЧС')
@allure.suite('Регресс для СТП')
@allure.sub_suite('Карточка происшествия')
@web_browser
class TestAccidentCard:

    @title('MCHS-1470: Сценарий создания карточки происшествия')
    @tms_link('MCHS-1470')
    @serial
    @pytest.mark.flaky(reruns=1)
    def test_mchs_1470(self, login_as, auth_api_client):
        suggest_address = AddressBuilder() \
            .with_full_address('"Проспект", Россия, Ростовская область, Белая Калитва, Ростовская улица, 1') \
            .with_country('Россия') \
            .with_subject('Ростовская область') \
            .with_city('Белая Калитва') \
            .with_object_('Проспект') \
            .with_street('Ростовская улица') \
            .with_house_number('1') \
            .with_address_description('Кинотеатр, Белокалитвинский район, Белокалитвенское городское поселение') \
            .build()

        sms_history_message = SmsHistoryBuilder().random().but() \
            .with_date(get_current_date()) \
            .with_status(SmsStatuses.READED) \
            .with_phone_number(PhoneNumbers.AON) \
            .build()

        call_records = RecordCallBuilder().with_empty_list().build()

        applicant_name_data = ApplicantNameBuilder().random().but().with_channel('МТС').with_foreign_language().build()

        incident = IncidentBuilder().with_user_arm(Users.SPECIALIST_1.arm).with_address(suggest_address).build()
        auth_api_client = auth_api_client(user=Users.SPECIALIST_1)
        auth_api_client.create_incident(incident)

        with allure.step("Шаг 1: Проверка отображения блоков в верхней части карточки"):
            new_card_page = login_as(Users.SPECIALIST_1).go_to_new_card_page_by_keyboard()
            new_card_page.close_other_tabs()
            new_card_page.aon_phone_container.is_active()
            new_card_page.telephony_container.assure_elements_is_visible()
            new_card_page.aon_phone_container.assure_elements_is_visible()
            new_card_page.location_phone_container.assure_elements_is_visible()
            new_card_page.provided_phone_container.assure_elements_is_visible()
            incident_id = new_card_page.get_browser_title()
            new_card_page.incident_container.assure_incident_container(
                title=incident_id,
                operator=Users.SPECIALIST_1,
            )
            new_card_page.timer_container.elements_is_visible()
        with allure.step("Шаг 2: Проверка заполнения блоков телефонов в верхней части карточки"):
            new_card_page.aon_phone_container.fill_phone(number=PhoneNumbers.AON)
            new_card_page.aon_phone_container.assure_phone(number=PhoneNumbers.AON)
            new_card_page.provided_phone_container.activate_by_keyboard()
            new_card_page.provided_phone_container.copy_aon_button_click()
            new_card_page.provided_phone_container.assure_phone(number=PhoneNumbers.AON)
            new_card_page.location_phone_container.activate_by_keyboard()
            new_card_page.location_phone_container.click_foreign_button()
            new_card_page.location_phone_container.fill_phone(PhoneNumbers.FOREIGN)
            new_card_page.location_phone_container.assure_phone(number=PhoneNumbers.FOREIGN)
        with allure.step("Шаг 4-8: Проверка отправки СМС"):
            new_card_page.aon_phone_container.activate_by_keyboard()
            create_sms_page = new_card_page.aon_phone_container.click_send_sms_button()
            create_sms_page.assure_dialog_container()
            new_card_page = create_sms_page.send_message(text=sms_history_message.text)
            sms_history_page = new_card_page.telephony_container.open_sms_history_list()
            sms_history_page.assure_dialog_container(form_data=sms_history_message)
            new_card_page = sms_history_page.click_return_to_card_button()
        with allure.step("Шаг 8-9: Проверка отсутствия звонков"):
            call_records_page = new_card_page.telephony_container.open_call_records()
            call_records_page.assure_dialog_container(form_data=call_records)
            new_card_page = call_records_page.close_page_by_keyboard()
        with allure.step("Шаг 10-13: Проверка блока заявителя"):
            new_card_page.applicant_name_container.activate_by_keyboard()
            new_card_page.applicant_name_container.assure_statuses(statuses=auth_api_client.get_reporter_statuses())
            new_card_page.applicant_name_container.fill_block(form_data=applicant_name_data)
            new_card_page.applicant_name_container.assure_block(form_data=applicant_name_data)
        with allure.step("Шаг 14-15: Проверка блока 'Адрес'"):
            new_card_page.address_container.activate_by_keyboard()
            new_card_page.address_container.assure_suggestions(
                value=f'''{suggest_address.subject,
                           suggest_address.city,
                           suggest_address.street,
                           suggest_address.house_number}''',
                yandex_suggest_count=3,
                fias_suggest_count=5)
            new_card_page.address_container.choose_address_from_suggest_list(value=suggest_address.full_address)
            new_card_page.address_container.assure_address(address=suggest_address)
        with allure.step("Шаг 16-17: Проверка блока 'Пострадавшие'"):
            new_card_page.injured_container.activate_by_keyboard()
            new_card_page.injured_container.assure_elements_is_visible()
            new_card_page.injured_container.assure_activate_count_input()
        with allure.step("Шаг 18: Проверка блока сохранения пустых карточек"):
            new_card_page.reject_container.activate_by_keyboard()
            new_card_page.reject_container.assure_elements_is_visible()
        with allure.step("Шаг 19-22: Проверка блока 'Что случилось'"):
            new_card_page.what_happens.activate_by_keyboard()
            new_card_page.what_happens.assure_elements_is_visible()
            answers = auth_api_client.get_report_answers(incident_id=incident_id.split(' ')[1])
            important_answers = auth_api_client.get_important_report_answers()
            new_card_page.what_happens.assure_answers(answers=answers, important_answers=important_answers)
            new_card_page.what_happens.choose_incident_type(incident=INCIDENTS['ДТП'].name)
            new_card_page.what_happens.assure_block_not_visible()
            new_card_page.question_list.assure_elements_is_visible()
            new_card_page.question_list.add_incident_type(incident='Аварии и происшествия в городском хозяйстве')
            new_card_page.branch_tags.assure_elements_is_visible()
            new_card_page.what_happens_content_branch_1.assure_content(incident_content=INCIDENTS['ДТП'].content)
            new_card_page.what_happens_content_branch_1.choose_answers(buttons=INCIDENTS['ДТП'].answers)
            new_card_page.what_happens_content_branch_1.check_answers_active_buttons(
                buttons=INCIDENTS['ДТП'].answers)
        with allure.step("Шаг 23: Проверка блока 'Описание со слов заявителя'"):
            new_card_page.description_container.activate_by_keyboard()
            new_card_page.description_container.fill_description(desc=sms_history_message.text)
            new_card_page.description_container.assert_char_counter(desc=sms_history_message.text)
        with allure.step("Шаг 24-27: Проверка блока служб"):
            add_service_window = new_card_page.footer_services_container.click_add_service_button()
            random_services_list = random_choice_items_from_list(iterable=auth_api_client.get_gos_services(),
                                                                 list_len=9)
            add_service_window.added_services(services=random_services_list)
            add_service_window.assure_added_services(services=random_services_list)
            new_card_page = add_service_window.save_and_close_button_click()
            new_card_page.footer_services_container.click_all_services_button()
            new_card_page.footer_services_container.assure_footer_services(services=random_services_list)
            new_card_page.footer_services_container.delete_service(service=random_services_list[0])
            new_card_page.footer_services_container.assure_footer_services(services=random_services_list[1:])
            new_card_page.footer_services_container.assure_all_services_button_not_visible()
        with allure.step("Шаг 28: Проверка всплывающего окна сохранения карточки"):
            save_incident_window = new_card_page.save_incident_window.open_window_by_keyword()
            save_incident_window.assure_elements_is_visible()
            save_incident_window.assure_services(services=random_services_list[1:])
            new_card_page = save_incident_window.click_return_to_fill_button()
        with allure.step("Шаг 29: Проверка всплывающего окна создания напоминания"):
            clock_alarm_window = new_card_page.clock_alarm_window.open_window_by_keyword()
            clock_alarm_window.assure_elements_is_visible()
            new_card_page = clock_alarm_window.click_cancel_button()
        with allure.step("Шаг 30-33: Проверка всплывающего окна создания связей"):
            accidents_list_window = new_card_page.accidents_list_window.open_window_by_keyword()
            accidents_list_window.activate_content_search_block()
            accidents_list_window.assure_time_input_is_enabled()
            accidents_list_window.activate_content_accidents_block()
            accidents_list_window.assure_expands_details_is_visible()
            accidents_list_window.activate_footer()
            accidents_list_window.assure_footer_is_enabled()
            new_card_page = accidents_list_window.return_to_card_by_keyboard()
        with allure.step("Шаг 34: Проверка всплывающего окна оповещения о происшествии"):
            notify_about_incident_window = new_card_page.notify_about_incident_window.open_window_by_keyword()
            notify_about_incident_window.assure_elements_is_visible()
            new_card_page = notify_about_incident_window.click_cancel_button()
        with allure.step("Шаг 35: Проверка всплывающего окна о закрытии карточки"):
            close_card_without_save_window = new_card_page.close_card_without_save_window.open_window_by_keyword()
            close_card_without_save_window.assure_elements_is_visible()
            new_card_page = close_card_without_save_window.click_return_to_fill_button()
        with allure.step("Шаг 36-40: Проверка опросных карт"):
            new_card_page.what_happens_content_branch_1.activate_by_keyboard()
            new_card_page.what_happens_content_branch_1.assure_answer_in_focus(answer_number=1)
            new_card_page.what_happens_content_branch_1.choose_first_answer_with_focus_by_keyboard()
            new_card_page.what_happens_content_branch_1.assure_answer_is_selected(answer_number=1)
            new_card_page.what_happens_content_branch_1.push_tab()
            new_card_page.what_happens_content_branch_1.assure_answer_in_focus(answer_number=2)
            new_card_page.what_happens_content_branch_2.activate_by_keyboard()
            new_card_page.what_happens_content_branch_2.assure_answer_in_focus(answer_number=1)
        with allure.step("Шаг 41: Проверка тултипов"):
            new_card_page.assure_tooltips_is_visible()
        with allure.step("Шаг 42: Проверка окна с дополнительным подтверждением вызываемых служб"):
            save_incident_window = new_card_page.footer_buttons_container.click_save_button()
            save_incident_window.assure_offline_services(services=random_services_list[1:])
        with allure.step("Шаг 43: Проверка сохраненной карточки"):
            saved_card_page = save_incident_window.click_notify_and_save_button()
            saved_card_page.close_other_tabs()
        with allure.step("Проверка телефонов"):
            saved_card_page.aon_phone_container.assure_phone(number=PhoneNumbers.AON)
            saved_card_page.provided_phone_container.assure_phone(number=PhoneNumbers.AON)
            saved_card_page.location_phone_container.assure_phone(number=PhoneNumbers.FOREIGN)
        with allure.step("Проверка блока оператор"):
            saved_card_page.incident_container.assure_incident_container(
                title=incident_id,
                operator=Users.SPECIALIST_1,
            )
        with allure.step("Проверка блока заявителя"):
            saved_card_page.applicant_name_container.assure_block(form_data=applicant_name_data)
        with allure.step("Проверка блока адрес"):
            saved_card_page.address_container.assure_address(address=suggest_address)
        with allure.step("Проверка блока 'Описание со слов заявителя'"):
            saved_card_page.description_container.assure_block(user=Users.SPECIALIST_1,
                                                               desc=sms_history_message.text)
        with allure.step("Проверка блока 'Что случилось'"):
            saved_card_page.what_happens.assure_answers(answers=INCIDENTS['ДТП'].answers)
            saved_card_page.what_happens.assure_count_items(count=2)
        with allure.step("Проверка кнопок Просмотр/Дополнение"):
            saved_card_page.view_mode_buttons_container.assure_buttons()
        with allure.step("Проверка блока отработок"):
            saved_card_page.workoff_container.assure_elements_is_visible()
        with allure.step("Проверка служб"):
            saved_card_page.footer_services_container.assure_footer_services(services=random_services_list[1:])
        with allure.step("Проверка кнопок в футере"):
            saved_card_page.footer_buttons_container.assure_buttons()
        with allure.step("Шаг 44-45: Проверка режима редактирования"):
            additional_mode_card_page = saved_card_page.view_mode_buttons_container.activate_additional_mode()
            additional_mode_card_page.question_list.add_incident_type(incident='103')
            additional_mode_card_page.wait_for_loading()
            additional_mode_card_page.what_happens_content_branch_1.assure_branch_is_visible()
            additional_mode_card_page.what_happens_content_branch_2.assure_branch_is_visible()
            additional_mode_card_page.what_happens_content_branch_3.assure_branch_is_visible()
            attention_not_save_window = additional_mode_card_page.added_but_not_save_window.open_window_by_keyword()
            attention_not_save_window.assure_elements_is_visible()
        with allure.step("Шаг 46: Проверка отсутствия дополнений"):
            additional_mode_card_page = attention_not_save_window.click_return_to_adding_button()
            attention_not_save_window = additional_mode_card_page.added_but_not_save_window.open_window_by_keyword()
            saved_card_page = attention_not_save_window.click_continue_without_saving_button()
            saved_card_page.wait_for_loading()
            saved_card_page.close_other_tabs()
            saved_card_page.what_happens.assure_count_items(count=2)

    @title('MCHS-1463: Блок Адрес')
    @tms_link('MCHS-1463')
    @serial
    def test_mchs_1463(self, login_as, auth_api_client):
        number_with_11_digits = str(get_random_number_with_digits_len(digits_len=11))
        number_with_16_digits = str(get_random_number_with_digits_len(digits_len=16))

        moscow_address = AddressBuilder() \
            .with_full_address('Москва Новая Бассманная 12') \
            .with_subject('Москва') \
            .with_city('Москва') \
            .with_street('Новая Бассманная') \
            .with_house_number('12') \
            .build()

        suggest_address = AddressBuilder() \
            .with_full_address('"Проспект", Россия, Ростовская область, Белая Калитва, Ростовская улица, 1') \
            .with_country('Россия') \
            .with_subject('Ростовская область') \
            .with_city('Белая Калитва') \
            .with_object_('Проспект') \
            .with_street('Ростовская улица') \
            .with_house_number('1') \
            .with_address_description('Кинотеатр, Белокалитвинский район, Белокалитвенское городское поселение') \
            .with_coordinates(longitude=40.754507, latitude=48.189475) \
            .build()

        address_for_16_step = AddressBuilder() \
            .with_street('Привольная') \
            .with_house_number('70') \
            .with_housing('3') \
            .build()
        full_address_for_16_step = AddressBuilder() \
            .with_country('Россия') \
            .with_subject('Москва') \
            .with_city('Москва') \
            .with_admin_area('ЮВАО') \
            .with_admin_district('Выхино-Жулебино') \
            .with_street(address_for_16_step.street) \
            .with_house_number(address_for_16_step.house_number) \
            .with_housing(address_for_16_step.housing) \
            .build()

        address_input_for_17_step = AddressBuilder() \
            .with_street('Евстафьева') \
            .with_house_number('3') \
            .build()

        address_for_18_step = AddressBuilder() \
            .with_subject('Московская область') \
            .with_street('Евстафьева') \
            .with_house_number('3') \
            .build()
        full_address_for_18_step = AddressBuilder() \
            .with_country('Россия') \
            .with_subject(address_for_18_step.subject) \
            .with_city('Балашиха') \
            .with_street(address_for_18_step.street) \
            .with_house_number(address_for_18_step.house_number) \
            .build()

        address_for_19_step = AddressBuilder() \
            .with_street('ghbdjkmyfz') \
            .with_building('1') \
            .with_housing('1') \
            .build()
        full_address_for_19_step = AddressBuilder() \
            .with_country('Россия') \
            .with_subject('Москва') \
            .with_city('Москва') \
            .with_admin_area('ЮВАО') \
            .with_admin_district('Выхино-Жулебино') \
            .with_street('Привольная улица') \
            .build()

        address_with_overflow_digits = AddressBuilder() \
            .with_house_number(number_with_11_digits) \
            .with_housing(number_with_11_digits) \
            .with_building(number_with_11_digits) \
            .with_flat(number_with_11_digits) \
            .with_entrance(number_with_11_digits) \
            .with_floor(number_with_16_digits) \
            .build()

        address_with_normal_digits = AddressBuilder() \
            .with_house_number(address_with_overflow_digits.house_number[:-1]) \
            .with_housing(address_with_overflow_digits.housing[:-1]) \
            .with_building(address_with_overflow_digits.building[:-1]) \
            .with_flat(address_with_overflow_digits.flat[:-1]) \
            .with_entrance(address_with_overflow_digits.entrance[:-1]) \
            .with_floor(address_with_overflow_digits.floor[:-1]) \
            .build()

        incident = IncidentBuilder().with_user_arm(Users.SPECIALIST_1.arm).with_address(suggest_address).build()
        auth_api_client = auth_api_client(user=Users.SPECIALIST_1)
        incident_id = auth_api_client.create_incident(incident)

        with allure.step("Шаг 1-3: Проверка значений по умолчанию и подсветки красным"):
            new_card_page = login_as(Users.SPECIALIST_1).go_to_new_card_page_by_keyboard()
            new_card_page.close_other_tabs()
            new_card_page.address_container.activate_by_keyboard()
            new_card_page.address_container.type_value_to_search_field(value=f'{moscow_address.street} '
                                                                             f'{moscow_address.house_number}')
            new_card_page.applicant_name_container.activate_by_keyboard()
            new_card_page.address_container.assure_full_address_is_red()
            new_card_page.address_container.assure_search_field(value=moscow_address.full_address)
        with allure.step("Шаг 4-5: Ввод совпадающего адреса и связывание карточек"):
            new_card_page.address_container.set_value_to_search_field(value=suggest_address.full_address)
            new_card_page.address_container.choose_address_from_suggest_list(value=suggest_address.full_address)
            accidents_address_repeated_page = new_card_page.address_container.click_concurrence_button()
            accidents_address_repeated_page.assure_elements_is_visible()
            new_card_page = accidents_address_repeated_page.bind_incident(incident_number=incident_id)
            new_card_page.footer_buttons_container.assure_card_linked_button()
        with allure.step("Шаг 6-7: Очистка адреса"):
            new_card_page.address_container.clean_address()
            new_card_page.address_container.assure_search_field(value=moscow_address.city)
            new_card_page.address_container.assure_input_field(field='Субъект', value=moscow_address.subject)
            new_card_page.address_container.assure_concurrence_button_is_not_visible()
            new_card_page.address_container.set_value_to_search_field(value=suggest_address.full_address)
            new_card_page.address_container.assure_value_not_in_search_field(value=moscow_address.city)
        with allure.step("Шаг 8-12: Проверка ограничения ввода 10-15 цифрами"):
            new_card_page.address_container.set_values_to_input_fields(address=address_with_overflow_digits)
            new_card_page.address_container.assure_address(address=address_with_normal_digits)
            new_card_page.close_other_tabs()

            new_card_page.address_container.clean_address()
            new_card_page.address_container.clean_address()
        with allure.step("Шаг 14-15: Получение и проверка местоположения"):
            new_card_page.aon_phone_container.fill_phone(number=PhoneNumbers.AON_FOR_LOCATION)
            new_card_page.aon_phone_container.click_get_location_button()
            new_card_page.address_container.assure_address_description_field(value=LOCATION_BY_AON_NUMBER)
            new_card_page.aon_phone_container.click_get_location_button()
            new_card_page.aon_phone_container.click_get_location_button()
            new_card_page.address_container.assure_address_description_field(value=LOCATION_BY_AON_NUMBER)
        with allure.step("Шаг 16: Проверка полей для адреса Улица: Привольная,  Дом: 70, Стр/соор: 3"):
            new_card_page.address_container.clean_address()
            new_card_page.address_container.set_values_to_input_fields(address=address_for_16_step)
            new_card_page.close_other_tabs()
            new_card_page.address_container.assure_address(address=full_address_for_16_step)
        with allure.step("Шаг 17: Проверка сообщения о том, что адрес не найден"):
            new_card_page.address_container.clean_address()
            new_card_page.address_container.set_values_to_input_fields(address=address_input_for_17_step)
            new_card_page.close_other_tabs()
            new_card_page.address_container.assure_address_not_found_message()
        with allure.step("Шаг 18: Проверка адреса в МО"):

            new_card_page.address_container.clean_address()
            new_card_page.address_container.clean_address()
            new_card_page.address_container.set_values_to_input_fields(address=address_for_18_step)
            new_card_page.close_other_tabs()
            new_card_page.address_container.assure_address(address=full_address_for_18_step)
        with allure.step("Шаг 19: Проверка переключения раскладки"):
            new_card_page.address_container.clean_address()
            new_card_page.address_container.set_values_to_input_fields(address=address_for_19_step)
            new_card_page.close_other_tabs()
            new_card_page.address_container.assure_address(address=full_address_for_19_step)
        with allure.step("Шаг 21-22: Проверка сортировки значений в дропдауне Округ"):
            new_card_page.address_container.assure_dropdown_list_sort(dropdown='Округ', value='ю')
            new_card_page.close_other_tabs()
        with allure.step("Шаг 23-24: Проверка сортировки значений в дропдауне Район"):
            new_card_page.address_container.assure_dropdown_list_sort(dropdown='Район', value='го')
            new_card_page.close_other_tabs()
        with allure.step("Шаг 25-26: Сохранение карточки"):
            new_card_page.address_container.set_value_to_search_field(value=suggest_address.full_address)
            new_card_page.address_container.choose_address_from_suggest_list(value=suggest_address.full_address)
            save_incident_window = new_card_page.footer_buttons_container.click_save_button_card_without_answers()
            saved_card_page = save_incident_window.click_save_card_button()
            saved_card_page.close_other_tabs()

    @title('MCHS-2115: Проверка наличия возможности добавлять отработки для разных ролей')
    @tms_link('MCHS-2115')
    @data_provider('user, flag', [
        (Users.EOS_OPERATOR, False),
        (Users.EOS_OBSERVER, False),
        (Users.EOS_CONTROLLER, False),
        (Users.CONTROL_OPERATOR, True),
        (Users.TELEPHONY_OPERATOR, False),
        (Users.SPECIALIST_1, True),
    ])
    def test_mchs_2115(self, login_as, auth_api_client, user, flag):
        with allure.step("Шаг 0 Подготовка тестовых данных"):
            incident_id = mchs_112_db_connect.get_last_incident_id_with_gos_service_id_and_incident_status_id(
                service_id=GosServices.SERVICE_101.id,
                incident_status_id=IncidentCardStatuses.REGISTERED.id)
            if not incident_id:
                incident_with_service_101 = IncidentBuilder() \
                    .with_user_arm(Users.SPECIALIST_1.arm) \
                    .with_gos_service_id(GosServices.SERVICE_101.id) \
                    .build()
                incident_id = auth_api_client(user=Users.SPECIALIST_1).create_incident(incident_with_service_101)

        with allure.step(f"Шаг 1-6 Проверка отображения кнопки под пользователем {user}"):
            search_page = login_as(user).close_other_tabs()
            card_page = search_page.go_to_incident_page(incident_id=incident_id)
            card_page.footer_buttons_container.assure_worked_out_button_is_visible(visible=flag)

    @title('MCHS-1162: Отработки')
    @tms_link('MCHS-1162')
    @serial
    def test_mchs_1162(self, login_as, auth_api_client):
        with allure.step("Шаг 0: Создание карточки, подготовка данных и авторизация"):
            incident = IncidentBuilder().with_user_arm(Users.SPECIALIST_1.arm).build()
            spec_1_auth_api_client = auth_api_client(user=Users.SPECIALIST_1)
            incident_id = spec_1_auth_api_client.create_incident(incident)
            search_page = login_as(Users.MAIN_SPECIALIST)
            search_page.close_other_tabs()

            workoff_form = WorkoffFormBuilder().random().but() \
                .with_operator_id(Users.MAIN_SPECIALIST.person_number) \
                .with_operator_arm(Users.MAIN_SPECIALIST.arm) \
                .with_start_date_time(get_current_date(format_string='%d.%m.%y %H:%M')) \
                .with_save_workoff_time(get_current_date(format_string='%H:%M')) \
                .with_service(GosServices.SERVICE_101.title) \
                .with_phone_number(GosServices.SERVICE_101.phone) \
                .build()

        with allure.step("Шаг 1-2: Открытие карточки и выбор службы"):
            saved_card_page = search_page.go_to_incident_page(incident_id=incident_id)
            saved_card_page.close_other_tabs()
            saved_card_page.workoff_container.open_service_dropdown_by_keyboard()
            saved_card_page.workoff_container.choose_service(service=GosServices.SERVICE_101.title)
        with allure.step("Шаг 3: Заполнение и проверка полей"):
            saved_card_page.workoff_container.fill_form(call_destination=workoff_form.call_destination,
                                                        username=workoff_form.username,
                                                        description=workoff_form.description)
            saved_card_page.workoff_container.save_form()
            saved_card_page.workoff_container.assure_last_row_form_data(form_data=workoff_form)
            saved_card_page.workoff_container.assure_last_row_color()
            saved_card_page.workoff_container.assure_last_row_tooltips(operator=Users.MAIN_SPECIALIST.name,
                                                                       call_destination=workoff_form.call_destination,
                                                                       username=workoff_form.username,
                                                                       description=workoff_form.description
                                                                       )
        with allure.step("Шаг 4: Переход в грид и проверка описания карточки"):
            search_page = saved_card_page.footer_buttons_container.click_close_button()
            search_page.close_other_tabs()
            search_page.table.expand_details_for_incident(incident_id=incident_id)
            search_page.table.assure_incident_last_workoff_data(form_data=workoff_form)
        with allure.step("Шаг 5: Проверка модального окна, с информацией о том что отработка не сохранена"):
            saved_card_page = search_page.go_to_incident_page(incident_id=incident_id)
            saved_card_page.close_other_tabs()
            saved_card_page.workoff_container.fill_form(
                service=GosServices.SERVICE_FSB.title,
                username=Users.SPECIALIST_1.name,
            )
            workoff_modal_window = saved_card_page.footer_buttons_container.click_close_button_with_unsaved_workoff()
            workoff_modal_window.assure_elements_is_visible()
        with allure.step("Шаг 6: Возврат в карточку"):
            saved_card_page = workoff_modal_window.click_return_to_workoff_button()
        with allure.step("Шаг 7: Закрытие карточки без сохранения, проверка отсутствия новой отработки"):
            workoff_modal_window = saved_card_page.footer_buttons_container.click_close_button_with_unsaved_workoff()
            search_page = workoff_modal_window.click_continue_without_saving_button()
            search_page.close_other_tabs()
            search_page.table.expand_details_for_incident(incident_id=incident_id)
            search_page.table.assure_incident_last_workoff_data(form_data=workoff_form)

    @title('MCHS-2117: Проставление статусов реагирования: проверка в КП при изменении в журнале')
    @tms_link('MCHS-2117')
    def test_mchs_2117(self, login_as, auth_api_client):
        with allure.step("Шаг 0: Создание карточки со службой ФСБ и авторизация"):
            incident_with_fsb_service = IncidentBuilder() \
                .with_user_arm(Users.SPECIALIST_1.arm) \
                .with_gos_service_id(GosServices.SERVICE_FSB.id) \
                .build()
            spec_1_auth_api_client = auth_api_client(user=Users.SPECIALIST_1)
            incident_with_fsb_service_id = spec_1_auth_api_client.create_incident(incident_with_fsb_service)
            search_page = login_as(Users.FSB_SPECIALIST)
            search_page.close_other_tabs()
        with allure.step("Шаг 1-5: Выбор и проверка статусов"):
            for status in [
                GosServicesStatuses.RECEIVED,
                GosServicesStatuses.ACCEPTED,
                GosServicesStatuses.START_RESPONSE,
                GosServicesStatuses.ARRIVED,
                GosServicesStatuses.EXECUTION_WORKS,
            ]:
                change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                    incident_id=incident_with_fsb_service_id)
                change_status_modal_window.choose_status(status)
                search_page = change_status_modal_window.save_and_close()
                search_page.wait_for_loading()
                card_page = search_page.go_to_incident_page(incident_id=incident_with_fsb_service_id)
                card_page.footer_services_container.assure_service_status(service=GosServices.SERVICE_FSB.title,
                                                                          status=status)
                search_page = card_page.go_to_search_page()
        with allure.step("Шаг 6: Выбор и проверка статуса 'Работы завершены', отображения тултипа"):
            change_status_modal_window = search_page.table.click_edit_service_status_button_for_incident(
                incident_id=incident_with_fsb_service_id)
            change_status_modal_window.choose_status(GosServicesStatuses.WORKS_FINISHED)
            search_page = change_status_modal_window.save_and_close()
            search_page.wait_for_loading()
            card_page = search_page.go_to_incident_page(incident_id=incident_with_fsb_service_id)
            card_page.footer_services_container.assure_service_status(service=GosServices.SERVICE_FSB.title,
                                                                      status=GosServicesStatuses.WORKS_FINISHED)
            card_page.footer_services_container.assure_edit_service_status_button_tooltip_is_visible(
                service=GosServices.SERVICE_FSB.title)

    @title('MCHS-2119: Проставление статусов реагирования: проверка в КП при изменении в КП')
    @tms_link('MCHS-2119')
    def test_mchs_2119(self, login_as, auth_api_client):
        with allure.step("Шаг 0: Создание карточки со службой ФСБ и авторизация"):
            incident_with_fsb_service = IncidentBuilder() \
                .with_user_arm(Users.SPECIALIST_1.arm) \
                .with_gos_service_id(GosServices.SERVICE_FSB.id) \
                .build()
            spec_1_auth_api_client = auth_api_client(user=Users.SPECIALIST_1)
            incident_with_fsb_service_id = spec_1_auth_api_client.create_incident(incident_with_fsb_service)
        with allure.step("Шаг 1: Открытие карточки"):
            search_page = login_as(Users.FSB_SPECIALIST).close_other_tabs()
            card_page = search_page.go_to_incident_page(incident_id=incident_with_fsb_service_id)
        with allure.step("Шаг 2-6: Выбор и проверка статусов"):
            card_page.footer_services_container.assure_service_status(service=GosServices.SERVICE_FSB.title,
                                                                      status=GosServicesStatuses.RECEIVED)
            for status in [
                GosServicesStatuses.ACCEPTED,
                GosServicesStatuses.START_RESPONSE,
                GosServicesStatuses.ARRIVED,
                GosServicesStatuses.EXECUTION_WORKS,
                GosServicesStatuses.WORKS_FINISHED,
            ]:
                gos_service_status_dialog = card_page.footer_services_container.open_gos_service_status_dialog(
                    service=GosServices.SERVICE_FSB.title)
                gos_service_status_dialog.choose_status(status=status)
                card_page = gos_service_status_dialog.click_save_button()
                card_page.footer_services_container.assure_service_status(service=GosServices.SERVICE_FSB.title,
                                                                          status=status)
            with allure.step("Проверка отображения tooltip у конечного статуса "):
                card_page.footer_services_container.assure_edit_service_status_button_tooltip_is_visible(
                    service=GosServices.SERVICE_FSB.title)
