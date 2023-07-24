from typing import List, TypeVar

from _python_core.http_codes import HTTPCode

ResponseGQLObject = TypeVar("ResponseGQLObject", bound="ResponseGQL")


class ResponseGQL:
    def __init__(
        self, code: HTTPCode, messages: List = [], errors: List = [], data: List = []
    ) -> None:
        self.code: int = code.value
        self.messages: List = messages
        self.errors: List = errors
        self.data: List = data
