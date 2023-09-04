import random
import string
from datetime import datetime

from data.fake_data import faker

garbage = '"¦O>”,“”‘~!@#$%^&*()?>,./\<][/*<!–”\",“${code}”;–>"'
ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RU = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
cyrillic_letters = ru + RU


class BaseBuilder:

    def __init__(self):
        self._faker = faker()

    def but(self):
        return self

    def get_random_cyr_string(self, char_count: int) -> str:
        """Получить случайный набор кириллических символов."""
        return self.random_id(length=char_count, is_latin=False, only_letters=True)

    def get_random_en_string(self, char_count: int) -> str:
        """Получить случайный набор латинских символов."""
        return self.random_id(length=char_count, is_latin=True, only_letters=True)

    @staticmethod
    def random_id(length: int = 8, strong: bool = False, is_latin: bool = True, only_letters: bool = False) -> str:
        """Получить случайный идентификатор, состоящий из цифр, букв или символов."""

        def mix_string(text: str) -> str:
            """Перемешать строку."""
            list_of_char = list(text)
            random.shuffle(list_of_char)
            return ''.join(list_of_char)

        rid = ''
        for x in range(length):
            rid += random.choice(
                mix_string(
                    ('!@#$%^&*()_-+=' if strong else '') +
                    (string.ascii_letters if is_latin else cyrillic_letters) +
                    (string.digits if not only_letters else '')
                )
            )
        return rid

    def generate_name(self, mask: str) -> str:
        """Сгенерировать случайное имя с префиксом."""
        return '{mask}_{stamp}_{rand_id}'.format(mask=mask, stamp=int(datetime.now().timestamp()),
                                                 rand_id=self.random_id(length=6))
