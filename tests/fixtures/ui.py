import pytest

from pages.login_page import LoginPage

__all__ = [
    "login_as",
]


@pytest.fixture
def login_as():
    def _login(user):
        main_page = LoginPage().login(user)
        return main_page

    return _login
