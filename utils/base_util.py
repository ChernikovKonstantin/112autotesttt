from pprint import pformat

import allure


class BaseUtil:
    def xprint(self, text, allure_title="Комментарий"):
        """ Вывод текста в консоль + attach в allure

        :param text: текст для вывода
        :param allure_title: метка в allure
        """
        formatted_text = pformat(text)
        allure.attach(formatted_text, allure_title, allure.attachment_type.TEXT)
        print(text)
