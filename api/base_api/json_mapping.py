from functools import wraps
from json import JSONDecodeError
from typing import List, Union, TypeVar, Type, cast

from requests import Response
from dacite import from_dict

from utils.service_utils import TestError
from .base_model import BaseModel

Model = TypeVar('Model', bound=BaseModel)


def mapping(response, cls):
    # type: (Response, Type[Model]) -> Union[Model, List['Model']]
    try:
        response_data = response.json()
    except JSONDecodeError as err:
        raise TestError(f'Response text: {response.text}\n{err}')
    if isinstance(response_data, list):
        return [cast(Model, from_dict(data_class=cls, data=item)) for item in response_data]
    else:
        return cast(Model, from_dict(data_class=cls, data=response_data))


def map_response(contract: Type[Model]):
    """
    Декоратор для конечных методов конректного Api класса.
    При включении режима маппинга в api классе (mapping=True, по дефолту) возвращает инстанс контракта
    При mapping=False возвращает чистый response

    :param contract: контакт ответа на запрос (positive or exception contract)
    :return: concrete contract or pure response
    """
    def wrapper(method):
        @wraps(method)
        def wrapped(self, *args, **kwargs):
            response = method(self, *args, **kwargs)
            status_code = response.status_code
            if self._mapping:
                if status_code == 200 and issubclass(contract, BaseModel):
                    return mapping(response, contract)
                if str(status_code).startswith('4') or str(status_code).startswith('5'):
                    raise AssertionError(f'Bad status code: {status_code}\nresponse: {response.text}')
                raise AssertionError(f'Unexpected status code: {status_code}\nresponse: {response.text}')
            return response

        return wrapped

    return wrapper
