from selene.api import s, be, command
from selene.core.entity import Element
from selene.core.exceptions import TimeoutException

from selene_custom import by


class BaseElement:
    """ Базовый класс кастомных элементов страницы. """

    def __init__(self, **kwargs):
        if len(kwargs) != 1:
            raise ValueError('Only one argument must be used')
        xpath_locator = kwargs.get('xpath', None)
        css_locator = kwargs.get('css', None)
        element = kwargs.get('element', None)
        if isinstance(xpath_locator, str):
            self._element = s(by.xpath(xpath_locator))
        elif isinstance(css_locator, str):
            self._element = s(css_locator)
        elif isinstance(element, Element):
            self._element = element
        else:
            raise TypeError('Wrong argument type')

    def waiting_to_be_visible(self, timeout=4):
        # type: (int) -> BaseElement
        self._element.with_(timeout=timeout).should(be.visible)
        return self

    def is_visible(self, timeout=4):
        # type: (int) -> bool
        try:
            self._element.with_(timeout=timeout).should(be.visible)
            return True
        except TimeoutException:
            return False

    def is_not_visible(self, timeout=4):
        # type: (int) -> bool
        try:
            self._element.with_(timeout=timeout).should(be.not_.visible)
            return True
        except TimeoutException:
            return False

    @property
    def element(self):
        # type: () -> Element
        return self._element

    def scroll_to(self):
        # type: () -> BaseElement
        self._element.with_(timeout=10).perform(command.js.scroll_into_view)
        return self

    def click(self):
        # type: () -> BaseElement
        self._element.click()
        return self
