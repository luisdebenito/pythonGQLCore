import os
import sys
from typing import List, Dict

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.responseGQL import ResponseGQL
from _python_core.http_codes import HTTPCode


def test_response() -> None:
    messages: List[str] = ["message_1", "message_2"]
    errors: List[str] = ["error1", "error2"]
    data: List[Dict] = [{"one": 1}, {"two": 2}]
    rsp = ResponseGQL(HTTPCode.CODE_200, messages, errors, data)

    assert rsp
    assert rsp.messages == messages
    assert rsp.errors == errors
    assert rsp.data == data
    assert rsp.code == HTTPCode.CODE_200.value
