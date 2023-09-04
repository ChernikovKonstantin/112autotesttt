__all__ = [
    'auth_api_client',
    'create_work_shift_group_with_main_specialist_and_users',
]

import allure
import pytest

from api.rest import RestApi
from data.fake_data import TestNames
from data.gos_services import GosServices
from data.users.user_list import User, Users
from database import mchs_112_db_connect


@pytest.fixture
def auth_api_client():
    def _login(user: User):
        return RestApi(user=user)

    return _login


@allure.step('Создание группы и добавление туда пользователей')
@pytest.fixture
def create_work_shift_group_with_main_specialist_and_users(auth_api_client):
    employee_id = Users.MAIN_SPECIALIST.id
    group_id = mchs_112_db_connect.get_value_from_staff_work_shift_group_by_employee_id(value='work_shift_group_id',
                                                                                        employee_id=employee_id)
    auth_client = auth_api_client(user=Users.SHIFT_SUPERVISOR)

    if group_id:
        auth_client.deactivate_work_shift_group(id_group=group_id)
    new_group_id = auth_client.create_work_shift_group(main_spec=Users.MAIN_SPECIALIST,
                                                       group_name=TestNames.WORK_SHIFT_GROUP).json()['id']
    for user in [Users.SPECIALIST_1, Users.MASHINISTOV_SPECIALIST]:
        auth_client.edit_work_shift_group(user_id=user.id,
                                          main_spec=Users.MAIN_SPECIALIST,
                                          group_name=TestNames.WORK_SHIFT_GROUP,
                                          group_id=new_group_id)
