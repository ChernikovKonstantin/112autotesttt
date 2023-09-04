from json import JSONDecodeError
from jsonschema import validate, ValidationError
from deepdiff import DeepDiff
from requests import Response

from api.base_api.base_model import BaseModel
from api.base_api.status_code import status_code as sc
from api.base_api.content_type import content_type as c_type
from utils.service_utils import action_on_error


class CheckList:

    def __init__(self, response: Response):
        self.response = response

    def _status_code_should_be(self, status_code: int):
        assert self.response.status_code == status_code
        return self

    def status_code_should_be_200(self):
        self._status_code_should_be(sc.SUCCESS)
        return self

    def status_code_should_be_202(self):
        self._status_code_should_be(sc.ACCEPTED)
        return self

    def status_code_should_be_400(self):
        self._status_code_should_be(sc.INCORRECT_HEADER)
        return self

    def status_code_should_be_403(self):
        self._status_code_should_be(sc.FORBIDDEN)
        return self

    def status_code_should_be_404(self):
        self._status_code_should_be(sc.NOT_FOUND)
        return self

    def status_code_should_be_405(self):
        self._status_code_should_be(sc.METHOD_NOT_ALLOWED)
        return self

    def _content_type_should_be(self, val: str):
        actual = self.response.headers['Content-Type'].lower().replace(' ', '')
        expected = val
        assert actual == expected, f'actual Content-Type header is not equal to expected: "{actual}" != "{expected}"'
        return self

    def content_type_should_be_json(self):
        self._content_type_should_be(c_type.JSON)
        return self

    def content_type_should_be_url_encoded(self):
        self._content_type_should_be(c_type.URL_ENCODED)
        return self

    def content_type_should_be_text(self):
        self._content_type_should_be(c_type.TEXT)
        return self

    def content_type_should_be_html(self):
        self._content_type_should_be(c_type.HTML)
        return self

    def content_type_should_be_pdf(self):
        self._content_type_should_be(c_type.PDF)
        return self

    def validate_json_schema(self, schema: dict):
        try:
            actual = self.response.json()
            try:
                validate(actual, schema)
                return self
            except ValidationError as err:
                action_on_error(err, is_scr=False)
        except JSONDecodeError as js_err:
            action_on_error(f"JSONDecodeError: {str(js_err)}\ntext response: {self.response.text}", is_scr=False)

    def response_text_is_equal(self, expected_text):
        assert self.response.text == expected_text
        return self

    def response_text_should_contains(self, string_part: str):
        assert string_part in self.response.text
        return self

    def response_json_is_equal(self, expected_dict, ignore_key=None, **kwargs):
        dict_compare(self.response.json(), expected_dict, ignore_key=ignore_key, **kwargs)
        return self

    def response_key_should_have_value(self, key, value):
        assert self.response.json()[key] == value
        return self

    def response_item_amount_is_equal(self, expected: int):
        actual = len(self.response.json())
        assert actual == expected, f'Response item amount is not equal to expected: "{actual}" != "{expected}"'
        return self


check_list = CheckList


def dict_compare(t1, t2, ignore_key=None, **kwargs):
    import re
    if isinstance(t1, BaseModel):
        t1 = t1.asdict()
    if isinstance(t2, BaseModel):
        t2 = t2.asdict()
    if ignore_key:
        ignore_key = re.split(r"[,;]", ignore_key)
        ignore_key = ["root['{0}']".format(el) for el in ignore_key]
    else:
        ignore_key = set()
    diffs = DeepDiff(t1, t2, exclude_paths=ignore_key, view='tree', **kwargs)
    if diffs:
        action_on_error(diffs, is_scr=False)
