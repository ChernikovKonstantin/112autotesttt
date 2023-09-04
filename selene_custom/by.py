from selene.support.by import *


# XPATH AXES LOCATORS
def be_following_sibling(with_tag: str = '*'):
    return xpath(f'./following-sibling::{with_tag}')


def next_element(order: int = 1):
    """
    Поиск элемента, находящегося на том же уровне после текущего
    :param order {int} - позиция нужного элемента, относительно текущего. Нумерация с 1.
    """
    return xpath(f'./following-sibling::*[{order}]')


def be_preceding_sibling(with_tag: str = '*'):
    return xpath(f'./preceding-sibling::{with_tag}')


def be_parent():
    return xpath('..')


# XPATH BY TEXT LOCATORS

def _escape_text_quotes_for_xpath(value: str):
    return 'concat("", "%s")' % (
        str(
            "\", '\"', \"".join(
                value.split('"'))))


def tag_text(tag_name: str, element_text: str):
    """
    Поиск тега с текстом
    :param tag_name: str
        название html тега
    :param element_text: str
        текст в элементе
    """
    return xpath(f'.//{tag_name}[text()[normalize-space(.) = '
                 + _escape_text_quotes_for_xpath(element_text)
                 + ']]')


def tag_partial_text(tag_name: str, element_text: str):
    """
    Поиск тега по частичному совпаданию текста
    :param tag_name: str
        название html тега
    :param element_text: str
        текст в элементе
    """
    return xpath(f'.//{tag_name}[text()[contains(normalize-space(.), '
                 + _escape_text_quotes_for_xpath(element_text)
                 + ')]]')


def label_text(element_text: str):
    """
    Поиск тега 'label' с текстом
    :param element_text: str
         текст в элементе
    """
    return tag_text('label', element_text)


def parent_label_text(element_text: str):
    """
    Поиск родительского элемента от тега 'label' с текстом
    :param element_text: str
        текст в элементе
    """
    return xpath('.//label[text()[normalize-space(.) = '
                 + _escape_text_quotes_for_xpath(element_text)
                 + ']]/..')


def button_text(element_text: str):
    """
    Поиск тега 'button' с текстом
    :param element_text: str
        текст в элементе
    """
    return tag_text('button', element_text)


def button_partial_text(element_text: str):
    """
    Поиск тега 'button' по частичному совпаданию текста
    :param element_text: str
        текст в элементе
    """
    return tag_partial_text('button', element_text)


def div_text(element_text: str):
    """
    Поиск тега 'div' с текстом
    :param element_text: str
        текст в элементе
    """
    return tag_text('div', element_text)


def div_partial_text(element_text: str):
    """
    Поиск тега 'div' по частичному совпаданию текста
    :param element_text: str
        текст в элементе
    """
    return tag_partial_text('div', element_text)


def span_text(element_text: str):
    """
    Поиск тега 'span' с текстом
    :param element_text: str
        текст в элементе
    """
    return tag_text('span', element_text)


def span_partial_text(element_text: str):
    """
    Поиск тега 'span' по частичному совпаданию текста
    :param element_text: str
        текст в элементе
    """
    return tag_partial_text('span', element_text)


def p_text(element_text: str):
    """
    Поиск тега 'p' с текстом
    :param element_text: str
        текст в элементе
    """
    return tag_text('p', element_text)
