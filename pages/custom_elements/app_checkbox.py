from __future__ import annotations

from selene_custom import query
from selene import be
from pages.common.base_element import BaseElement


class AppCheckbox(BaseElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_value(self, status: bool) -> AppCheckbox:
        current_status = self.is_checked()
        if status != current_status:
            self._element.should(be.enabled).click()
        return self

    def is_checked(self):
        # type: () -> bool
        return 'active' in self._element.get(query.class_value)
