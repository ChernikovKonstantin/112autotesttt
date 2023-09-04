from pprint import pformat
from typing import Union

import allure
from selene.core.entity import Element


class PrintMixin:
    """Распечатка свойств объекта в читаемом виде."""

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{class_name}.{key}={value}".format(class_name=self.__class__.__name__.lower(),
                                                          key=key, value=self.__dict__[key]))
        return '\n'.join(sb)

    def __repr__(self):
        return self.__str__()


class TestError(Exception):
    def __init__(self, msg):
        self.value = msg

    def __str__(self):
        return self.value


def wait_seconds(second: Union[int, float] = 1) -> None:
    """Обертка под time.sleep."""
    from time import sleep
    sleep(second)


def format_text_error(error):
    """Возвращает отформатированный текст ошибки для функции action_on_error(),
    если переданный параметр text является списком."""
    text_part = 'Обнаружены ошибки %s шт:\n%s'
    if isinstance(error, list):
        return text_part % (len(error), '\n'.join(error))
    return error


def screenshot_page():
    """Сделать скриншот страницы."""
    from selene.api import browser
    allure.attach(browser.driver.get_screenshot_as_png(), 'Screenshot', allure.attachment_type.PNG)


def print_and_logging(text, text_name='Комментарий'):
    """Объединены функции print и allure.attach."""
    formatted_text = pformat(text)
    allure.attach(formatted_text, text_name, allure.attachment_type.TEXT)
    print(formatted_text)


def action_on_error(text='Проверка завершилась с ошибкой', title='Error', is_scr=True):
    """
    :param text: {str} текст комментария
    :param title: {str} название пункта в отчете
    :param is_scr: {bool}: делать ли скриншот
    """
    if is_scr:
        screenshot_page()
    text = format_text_error(text)
    print_and_logging(text, text_name=title)
    assert False, text


def action_on_success(is_scr=False):
    """
    :param is_scr: {bool}: делать ли скриншот
    """
    with allure.step('Success'):
        if is_scr:
            screenshot_page()


def on_attribute_error_return_false(no_args_predicate):
    """Возращает False, если вызвается исключение AttributeError.
    Пример использования:
        on_attribute_error_return_false(lambda: instance.attribute) """
    try:
        return no_args_predicate()
    except AttributeError:
        return False


def random_choice_with_exclude(iterable, exclude=None):
    """
    Случайный элемент из списка с возможностью задать список исключаемых элементов.
    Не использовать для сложных типов данных. Только для неизменямых типов.
    """
    from random import choice
    if not isinstance(exclude, list):
        exclude = [exclude]
    return choice([item for item in iterable if item not in exclude])


def convert_utc_date_to_local(date):
    """
    :param date: datetime object
    :return: str
    """
    import pytz
    return date.replace(tzinfo=pytz.utc).astimezone()


def parse_date(date: str, **kwargs):
    """
    Парсит строку с датой и переводит в объект datetime
    timezone issue: https://www.linux.org.ru/forum/development/13640755
    :param date: str
    :return: datetime
    """
    import pytz
    from dateutil.parser import parse
    tz = pytz.timezone('Europe/Moscow')
    return parse(date, **kwargs).astimezone(tz)


def reformat_date(date, format_string="%d.%m.%Y %H:%M:%S"):
    # type: (str, str) -> str
    """ Принимает строку с датой, переформатирует в указанный формат."""
    return parse_date(date).strftime(format_string)


def calculate_age(birthday: str, **kwargs) -> int:
    """
    Рассчитывает количество полных лет
    :param birthday: str
        - дата рождения в формате (если dd.mm.YYYY, то нужно использовать dayfirst=True)
    :param kwargs: Any
          - см доку по dateutil.parser.parse
    :return: int
    """
    from datetime import date
    born = parse_date(birthday, **kwargs)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def calculate_age_with_suffix(birthday: str, **kwargs) -> str:
    """
    Рассчитывает количество полных лет и суффикс
    :param birthday: str
        - дата рождения в формате (если dd.mm.YYYY, то нужно использовать dayfirst=True)
    :param kwargs: Any
          - см доку по dateutil.parser.parse
    :return: str
    """
    age = calculate_age(birthday, **kwargs)
    suffix = ("год" if 11 <= age <= 19 or age % 10 == 1 else
              "года" if 2 <= age % 10 <= 4 else
              "лет")
    return f'{age} {suffix}'


MONTH_REPLACE = {
    'января': 'jan',
    'февраля': 'feb',
    'марта': 'mar',
    'апреля': 'apr',
    'мая': 'may',
    'июня': 'jun',
    'июля': 'jul',
    'августа': 'aug',
    'сентября': 'sep',
    'октября': 'oct',
    'ноября': 'nov',
    'декабря': 'dec'
}


def multi_replace(text: str, replacement: dict) -> str:
    """
    Множественная замена в тексте по словарю
    :param text: str - текст, в которым нужно провести замену
    :param replacement: dict - словарь с заменами
    :return: str - текст с замененными значениями
    """
    import re
    # use these three lines to do the replacement
    replacement = dict((re.escape(k), v) for k, v in replacement.items())
    # Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
    pattern = re.compile("|".join(replacement.keys()))
    text = pattern.sub(lambda m: replacement[re.escape(m.group(0))], text)
    return text


def replace_cyrillic_month(text: str) -> str:
    """
    Заменяет русские названия месяца в в род. падеже на сокращенные английские названия
    :param text: исходный текст
    :return: str: измененный текст
    """
    return multi_replace(text, MONTH_REPLACE)


def convert_bytes_to_base64(obj: bytes, encoding: str = 'utf-8') -> str:
    """Конвертирует байты в строку base64."""
    import base64
    return base64.b64encode(obj).decode(encoding)


def clean_phone_number(number: str) -> str:
    """Очистка номера телефона от символов +/s()-."""
    import re
    return re.sub(r'[+\s()-]', '', number)


def get_int_from_text(text: str) -> int:
    """Возвращает цифры из текста"""
    import re
    result = re.search(r'\d+', text)
    return int(result.group(0))


def get_zip_archive_file_list(response):
    """
    Возвращает список из названий файлов и их размера в zip-архиве
    :param response: requests.Response
    :return: List[str, str]
    """
    import io
    import zipfile
    result = []
    archive = zipfile.ZipFile(io.BytesIO(response.content))
    for entry in archive.infolist():
        name = entry.filename.encode('cp437').decode('cp866')
        size = entry.file_size
        result.append([name, size])
    return result


def format_number_with_spaces(number: Union[int, float]) -> str:
    """
    Выделяет разряды числа пробелами
    :param number: int
    :return: str
    """
    return '{0:,}'.format(number).replace(',', ' ')


def transliterate(text_value):
    # type: (str) -> str
    """Транслитерация кириллицы в латиницу."""
    # Словарь с заменами
    replacement = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
                   'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                   'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                   'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
                   'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
                   'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
                   'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
                   'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
                   'Ю': 'U', 'Я': 'YA'}
    return text_value.translate(str.maketrans(replacement))


def _get_element_color(element: Element, css_property: str):
    from selenium.webdriver.support.color import Color
    from selene_custom import query
    el_color = element.get(query.css_property(css_property))
    return Color.from_string(el_color).hex


def get_text_color(element: Element) -> str:
    return _get_element_color(element, 'color')


def get_background_color(element: Element) -> str:
    return _get_element_color(element, 'background-color')


def get_outline_color(element: Element) -> str:
    return _get_element_color(element, 'outline-color')


def get_large_text():
    from data.fake_data import faker
    return faker().text(max_nb_chars=2000)


def get_text_with_max_nb_chars(max_nb_chars: int = 2000):
    from data.fake_data import faker
    return faker().text(max_nb_chars=max_nb_chars)


def get_first_string_from_text(value: str):
    return str(value.splitlines()[0]).strip('[\']')


def get_random_number() -> int:
    import random
    return random.choice(range(1000, 9999999))


def get_random_number_with_digits_len(digits_len: int) -> int:
    from data.fake_data import faker
    return faker().random_number(digits=digits_len, fix_len=True)


def random_choice_items_from_list(iterable, list_len: int):
    """
    Возвращает случайный набор неповторяющихся значений из списка.
    """
    from random import choice
    items_list = []
    while len(items_list) < list_len:
        random_choice = choice(iterable)
        if random_choice not in items_list:
            items_list.append(random_choice)
    return items_list


if __name__ == '__main__':
    pass
