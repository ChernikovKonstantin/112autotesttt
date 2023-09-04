import json
import os

import allure
import pytest
from selene.common.helpers import on_error_return_false
from selene.support.shared import config as selene_config
from selene.api import browser
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from conf.browser_name import BrowserName
from conf.conf import Conf
from conf.stand import get_stand_data
from .fixtures import *  # do not delete!


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default='stb')
    parser.addoption("--browser", action="store", default=BrowserName.CHROME)
    parser.addoption("--browser_ver", action="store", default="")
    parser.addoption("--headless", action="store_true", default=False)
    parser.addoption("--remote", action="store_true", default=False)
    parser.addoption("--hub", action="store", default="172.17.21.145")
    parser.addoption("--port", action="store", default="4444")
    parser.addoption("--download_path", action="store", default=f"{os.path.join(os.getcwd(), 'download')}")


def pytest_configure(config):
    """ Добавляем переменные среды. """
    import os
    os.environ['ENV'] = config.getoption('--env')


@pytest.fixture(scope='session', autouse=True)
def config(request):
    conf = Conf()
    # stand = request.config.getoption("--stand")
    stand = get_stand_data().ui
    browser_name = request.config.getoption("--browser")
    version = request.config.getoption("--browser_ver")
    hub = request.config.getoption("--hub")
    port = request.config.getoption("--port")
    headless = request.config.getoption("--headless")
    remote = request.config.getoption("--remote")
    download_path = request.config.getoption("--download_path")
    conf.configuration.update(
        {"stand": stand,
         "browser": browser_name,
         "version": version,
         "hub": hub,
         "port": port,
         "headless": headless,
         "remote": remote,
         "download_path": download_path,
         })
    return conf.configuration


def get_chrome_options(config):
    options = ChromeOptions()
    options.headless = config["headless"]
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--kiosk-printing")
    options.add_argument(f'--print-to-pdf={config["download_path"]}')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    appState = {
        "recentDestinations": [
            {
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }

    options.add_experimental_option("prefs", {
        "download.default_directory": config["download_path"] if not config["remote"] else "/home/selenium/Downloads",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        'printing.print_preview_sticky_settings.appState': json.dumps(appState),
        "safebrowsing.enabled": True,
    })
    return options


def get_firefox_options(config):
    options = FirefoxOptions()
    options.headless = config["headless"]
    return options


def create_remote_driver(config):
    if config["browser"] == BrowserName.CHROME:
        options = get_chrome_options(config)
    elif config["browser"] == BrowserName.FIREFOX:
        options = get_firefox_options(config)
    else:
        raise ValueError('Please specify valid browser name')
    capabilities = {"browserName": config["browser"],
                    "version": config["version"],
                    "acceptInsecureCerts": True,
                    "name": 'mchs112-stb',
                    "enableVNC": True,
                    "enableLog": True,
                    "timeZone": "Europe/Moscow",
                    "hostsEntries": ["ispro-test2.mos.ru:172.17.40.23", "ispro-test.mos.ru:10.15.141.129"],
                    "env": ["VERBOSE=1"]
                    }
    driver = webdriver.Remote(command_executor=f'http://test:test@{config["hub"]}:{config["port"]}/wd/hub',
                              options=options,
                              desired_capabilities=capabilities)
    return driver


def create_local_driver(config):
    if config["browser"] == BrowserName.CHROME:
        driver_manager = ChromeDriverManager()
        options = get_chrome_options(config)
        #driver = webdriver.Chrome(executable_path=driver_manager.install(), options=options)
        driver = webdriver.Chrome(executable_path="C:/Python310/chromedriver.exe", options=options)
    elif config["browser"] == BrowserName.FIREFOX:
        driver_manager = GeckoDriverManager()
        options = get_firefox_options(config)
        driver = webdriver.Firefox(executable_path=driver_manager.install(), options=options)
    else:
        raise ValueError('Please specify valid browser name')
    return driver


@pytest.fixture(scope='function')
def web_browser(request, config):
    if config["remote"]:
        driver = create_remote_driver(config)
    else:
        driver = create_local_driver(config)
    if not config["headless"]:
        driver.set_window_size(1680, 900)  # один размер для локального/удаленного запуска
    # config selene  browser
    selene_config.save_screenshot_on_failure = False
    selene_config.save_page_source_on_failure = False
    selene_config.timeout = 4
    selene_config.driver = driver
    selene_config.base_url = f'https://{config["stand"]}'
    yield
    selene_config.quit_driver()


def pytest_exception_interact():
    from pprint import pformat
    # if driver is running, make screenshot and get logs
    if on_error_return_false(lambda: browser.driver.title is not None):
        allure.attach(browser.driver.get_screenshot_as_png(), name='failure-screenshot',
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(pformat(browser.driver.get_log('browser')), name='js-console-log',
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(pformat(browser.driver.get_log('driver')), name='driver-log',
                      attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope='session')
def resource_path():
    """
    Формирует путь до файла с ресурсом
    """

    def _path(file_name: str):
        import os
        return os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), f'..{os.sep}resources', file_name))

    return _path
