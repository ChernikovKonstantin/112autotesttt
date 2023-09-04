import pytest
import allure

# web browser
web_browser = pytest.mark.usefixtures("web_browser")

# selenoid api
selenoid_api = pytest.mark.usefixtures('selenoid_api')

# allure report
title = allure.title
dynamic_title = allure.dynamic.title

# allure custom suites
mayor_scenario = allure.parent_suite('Сценарии Мэрии')
direct_scenario = allure.suite('Прямые сценарии')

PROJECT_PREFIX = 'OOG'


def jira_link(short_name):
    url = f'type_url{short_name}'
    return allure.issue(url, short_name)


# allure report links to ticket management system
def tms_link(short_name):
    url = f'http://172.17.21.63/testlink/linkto.php?tprojectPrefix={PROJECT_PREFIX}&item=testcase&id={short_name}'
    return allure.testcase(url, name=f'TestLink: {short_name}')


skip = pytest.mark.skipif(True, reason='Временно не запускаем')
not_ready = pytest.mark.skipif(True, reason='Тест находится в разработке')
xfail = pytest.mark.xfail(strict=True)  # тест всегда проваливается (оформлен баг) #params: reason: str

serial = pytest.mark.serial  # запуск тестов последовательно
smoke = pytest.mark.smoke  # набор для smoke-тестирования
regress = pytest.mark.regress  # набор для regress-тестирования

data_provider = pytest.mark.parametrize  # параметризированные тесты
flaky = pytest.mark.flaky  # нестабильные тесты # params: reruns: int, reruns_delay: int
