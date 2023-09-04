import allure

from api.base_api.common_check import check_list
from api.base_api_112 import BaseApi112
from api.end_point import EndPoint
from conf.stand import get_stand_data
from data.builders.incident_builder import IncidentFormData
from data.users.user_list import User


class RestApi(BaseApi112):

    def __init__(self, user: User):
        super().__init__()
        self.stand = get_stand_data()
        self.login(user)
        self._http_client.session.headers = {
            'X-CSRF-TOKEN': self._http_client.session.cookies._cookies[self.stand.ui]['/']['XSRF-TOKEN'].value,
        }

    @allure.step('Получение часто выбираемых тегов')
    def get_report_answers(self, incident_id: str):
        response = self.get(f'{EndPoint.new_incident_card}',
                            params={'id': incident_id, 'isSave': 'true'}).json()
        return [item['title'] for item in response['reportList']['reportTransferList'][0]['reportAnswerList']]

    @allure.step('Получение списка значимых типов происшествий')
    def get_important_report_answers(self):
        response = self.get(f'{EndPoint.important_answers}').json()
        return [item['title'] for item in response]

    @allure.step('Получение статусов звонившего')
    def get_reporter_statuses(self):
        response = self.get(f'{EndPoint.reporter_statuses}').json()
        return [item['right'] for item in response]

    @allure.step('Получение шаблонов сообщений')
    def get_message_templates(self):
        response = self.get(f'{EndPoint.templates}').json()
        return [item['template'] for item in response]

    @allure.step('Получение списка служб')
    def get_gos_services(self):
        response = self.get(f'{EndPoint.gos_service}').json()
        return [item for item in response if
                item['visible'] and len(item['shortTitle']) > 2 and "\"" not in item['fullTitle']]

    @allure.step('Получение id нового инцидента')
    def get_new_incident_number(self, work_place: str):
        response = self.post(f'{EndPoint.get_new_incident}',
                             params={'workPlace': int(work_place), 'manuallyCreated': 'true'})
        check_list(response).status_code_should_be_200()
        return str(response.json())

    @allure.step('Сохранение адреса инцидента')
    def save_incident_address(self, address: dict, incident_id: int):
        response = self.post(f'{EndPoint.save_address}{incident_id}', json=address)
        check_list(response).status_code_should_be_200()
        return response

    @allure.step('Сохранение пострадавших')
    def save_incident_injured(self, injured_count: str, incident_id: int):
        response = self.post(f'{EndPoint.save_injured}{incident_id}', json={
            'hasInjured': True,
            'injuredCount': injured_count
        })
        check_list(response).status_code_should_be_200()
        return response

    @allure.step('Сохранение службы')
    def save_gos_service(self, incident_id: str, save_gos_service_id: int):
        response = self.post(f'{EndPoint.save_gos_services}{incident_id}', json=[{
            'id': save_gos_service_id,
            'network': 1,
            'emergencySending': False
        }])
        check_list(response).status_code_should_be_200()
        return response

    @allure.step('Регистрация инцидента')
    def register_incident(self, incident_id: int):
        response = self.post(f'{EndPoint.register_incident}{incident_id}',
                             json={'saveList': [], 'descriptionList': [{}], 'address': {}, 'reporterList': [{}],
                                   'gosServiceList': [], 'reportList': {}, 'emptyType': None, 'occurrence': False})
        check_list(response).status_code_should_be_200()
        return response

    @allure.step('Создание карточки')
    def create_incident(self, data: IncidentFormData):
        id_ = self.get_new_incident_number(work_place=data.user_arm)
        if data.address:
            address = {'street': data.address.street,
                       'country': data.address.country,
                       'city': data.address.city,
                       'region': data.address.subject,
                       'object': data.address.object_,
                       'numberOnStreet': data.address.house_number,
                       'building': data.address.building,
                       'corpus': data.address.housing,
                       'entrance': data.address.entrance,
                       'kodDomofon': data.address.entrance_code,
                       'apartment': data.address.flat,
                       'floor': data.address.floor,
                       'description': data.address.address_description,
                       'longitude': data.address.longitude,
                       'latitude': data.address.latitude}
            self.save_incident_address(incident_id=id_, address=address)
        if data.injured_count:
            self.save_incident_injured(incident_id=id_, injured_count=data.injured_count)
        if data.gos_service_id:
            self.save_gos_service(incident_id=id_, save_gos_service_id=data.gos_service_id)
        self.register_incident(incident_id=id_)
        return id_

    @allure.step('Связывание карточек')
    def bind_cards(self, parent_incident_id: int, incident_id: str):
        response = self.post(f'{EndPoint.create_chain_incident}',
                             json={'incidentId': incident_id, 'parentIncidentId': parent_incident_id})
        check_list(response).status_code_should_be_200()
        return response

    @allure.step('Деактивация группы рабочей смены')
    def deactivate_work_shift_group(self, id_group: int):
        response = self.post(f'{EndPoint.deactivate_work_shift_group}{id_group}')
        check_list(response).status_code_should_be_200()
        return response

    @allure.step('Создание группы рабочей смены')
    def create_work_shift_group(self, main_spec: User, group_name: str):
        response = self.post(f'{EndPoint.create_work_shift_group}',
                             json={'employeeLead': {'id': main_spec.id,
                                                    'firstName': '',
                                                    'lastName': '',
                                                    'secondName': '',
                                                    'age': '', 'experience': '', 'description': '',
                                                    'login': main_spec.login,
                                                    'personNumber': main_spec.person_number,
                                                    'gosServiceTitle': None,
                                                    'shortFio': main_spec.name_with_dots, 'workPlace': 33,
                                                    'avayaStatus': 'NOT_CONNECTED', 'extraNumber': None,
                                                    'ipPhone': 12345, 'fio': main_spec.name_with_dots},
                                   'name': group_name})
        check_list(response).status_code_should_be_200()
        return response

    @allure.step('Редактирование группы рабочей смены')
    def edit_work_shift_group(self, user_id: int, main_spec: User, group_id: int, group_name: str):
        response = self.post(f'{EndPoint.edit_staff_shift_group}{user_id}',
                             json={'id': group_id,
                                   'employeeLead': {'id': main_spec.id, 'arm': main_spec.arm,
                                                    'firstName': '',
                                                    'lastName': '', 'secondName': '',
                                                    'personNumber': main_spec.person_number,
                                                    'fio': main_spec.name_with_dots,
                                                    'authRole': 'LEAD_SPECIALIST'},
                                   'name': group_name})
        check_list(response).status_code_should_be_200()
        return response
