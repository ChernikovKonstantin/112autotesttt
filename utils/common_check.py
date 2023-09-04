from typing import Union

import allure
from selene.api import browser, have
from selene.core.entity import Element, Collection
from selene.core.exceptions import TimeoutException
from selene.support.conditions import be

from utils.service_utils import action_on_error
from utils.text_extractor import extract_text_from_pdf, extract_text_from_doc, extract_text_from_docx


@allure.step('Проверка титула страницы')
def assure_browser_title(expected_title: str, timeout: int = 4):
    browser.with_(timeout=timeout).should(have.title(expected_title))


@allure.step('Проверка: титул страницы содержит текст')
def assure_browser_title_contains_text(expected_text: str, timeout: int = 4):
    browser.with_(timeout=timeout).should(have.title_containing(expected_text))


@allure.step('Проверка адреса страницы')
def assure_current_page_url(expected_url: str, timeout: int = 4):
    try:
        browser.with_(timeout=timeout).should(have.url(expected_url))
    except TimeoutException as reason:
        raise AssertionError(f'Не удалось перейти на страницу:\n{reason}')


@allure.step('Проверка: адрес страницы содержит текст')
def assure_current_page_url_contains_text(expected_text: str, timeout: int = 4):
    try:
        browser.with_(timeout=timeout).should(have.url_containing(expected_text))
    except TimeoutException as reason:
        raise AssertionError(f'Не удалось перейти на страницу:\n{reason}')


@allure.step('Проверка наличия элемента на странице')
def assure_current_page_contains_element(element: Element):
    try:
        element.with_(timeout=10).should(be.present)
    except Exception as ex:
        assert False, f"ERROR: page not contains element.\n{ex}"


@allure.step('Проверка отсутствия элемента на странице')
def assure_current_page_is_absent_element(element: Element):
    try:
        element.with_(timeout=10).should(be.not_.present)
    except Exception as ex:
        assert False, f"ERROR: page is contains element.\n{ex}"


@allure.step('Проверка доступности элемента на странице')
def assure_current_page_element_enable(element: Element):
    try:
        element.with_(timeout=10).should(be.enabled)
    except Exception as ex:
        assert False, f"ERROR: element is not enabled.\n{ex}"


@allure.step('Проверка недоступности элемента на странице')
def assure_current_page_element_disabled(element: Element):
    try:
        element.with_(timeout=10).matching(be.disabled)
    except Exception as ex:
        assert False, f"ERROR: element is not disabled.\n{ex}"


@allure.step('Проверка кликабельности элемента на странице')
def assure_current_page_element_clickable(element: Element):
    try:
        element.with_(timeout=10).should(be.clickable)
    except Exception as ex:
        assert False, f"ERROR: element is not clickable.\n{ex}"


@allure.step('Проверка: размер загруженного файла')
def assure_downloaded_file_size(response, expected_value: int):
    actual_file_size = int(response.headers['Content-Length'])
    assert actual_file_size == expected_value, \
        f'ERROR: actual file size: {actual_file_size} != expected size: {expected_value}'


@allure.step('Проверка: значения есть в тексте')
def assure_that_values_in_text(text_content, *values, screenshot=True):
    errors = []
    for val in values:
        if val not in text_content:
            errors.append(f'ERROR: {val} NOT IN {text_content}')
    if errors:
        action_on_error(errors, is_scr=screenshot)


@allure.step('Проверка: в pdf-файле есть текст')
def assure_that_pdf_file_contains_text(pdf_content, *expected: str, ignore_line_break=False, screenshot=True):
    extracted_text = extract_text_from_pdf(pdf_content)
    if ignore_line_break:
        extracted_text = extracted_text.replace('\n', ' ')
    assure_that_values_in_text(extracted_text, *expected, screenshot=screenshot)


@allure.step('Проверка: в doc-файле есть текст')
def assure_that_doc_file_contains_text(doc_content, *expected: str, encoding='utf-8'):
    extracted_text = extract_text_from_doc(doc_content, encoding)
    assure_that_values_in_text(extracted_text, *expected)


@allure.step('Проверка: в docx-файле есть текст')
def assure_that_docx_file_contains_text(doc_content, *expected: str):
    extracted_text = extract_text_from_docx(doc_content)
    assure_that_values_in_text(extracted_text, *expected)


@allure.step('Сравнение данных')
def dict_compare(actual, expected, ignore_key=None, is_src=True, **kwargs):
    import re
    from deepdiff import DeepDiff
    if ignore_key:
        ignore_key = re.split(r"[,;]", ignore_key)
        ignore_key = ["root['{0}']".format(el) for el in ignore_key]
    else:
        ignore_key = set()
    diffs = DeepDiff(actual, expected, exclude_paths=ignore_key, view='tree', **kwargs)
    if diffs:
        action_on_error(diffs, is_scr=is_src)


@allure.step('Проверка текста статуса элемента')
def assure_element_has_status_text(element: Element, expected_text: str) -> bool:
    if expected_text:
        from selene_custom import query
        return expected_text == element.get(query.text)
    else:
        try:
            assure_current_page_is_absent_element(element)
        except AssertionError:
            return False
        return True


@allure.step('Сравнение данных')
def compare_tuple(in_list: Collection, expected: Union[str, tuple]) -> bool:
    from selene_custom import query
    if isinstance(expected, str):
        expected = (expected,)
    actual = tuple([x.get(query.text) for x in in_list])
    for e, a in zip(expected, actual):
        try:
            assert e == a and len(expected) == len(actual)
        except AssertionError:
            return False
    return True
