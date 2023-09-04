import allure

from typing import Optional

from api.base_api.base_api import BaseApi
from api.base_api.common_check import check_list
from api.end_point import EndPoint
from conf.stand import Stand
from conf.stand import get_stand_data
from data.cards_data import JSON_TO_EXTERNAL_SERVICE
from data.users.user_list import User


class BaseApi112(BaseApi):
    def __init__(self, stand: Optional[Stand] = None):
        self.stand = stand if stand else get_stand_data()
        super().__init__(api_host=f'https://{self.stand.ui}', timeout=60)

    @allure.step('Авторизация')
    def login(self, user: User):
        payload = {'username': user.login,
                   'password': user.password,
                   'workPlace': user.arm,
                   'rememberMe': True}
        response = self.post(f'https://{self.stand.ui}{EndPoint.login}', data=payload)

        check_list(response).status_code_should_be_200()
        return self

    @allure.step('Отправка карточки из внешнего сервиса')
    def send_new_card_from_external_service(self):
        response = self.post(f'https://{self.stand.db}/api/v2/incident/sendnewcard', json=JSON_TO_EXTERNAL_SERVICE)
        check_list(response).status_code_should_be_200()
        return response.json()['cardId']

    if __name__ == '__main__':
        pass
