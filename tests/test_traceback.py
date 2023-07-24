import os
import sys
import traceback
import json
from typing import Dict, List, Tuple
import pytest

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.mytraceback import TraceBack


class Headers:
    def __init__(self, header: Tuple) -> None:
        self.raw: List[Tuple] = [header]


class TestTraceBack:
    def test_simple_no_matching_type(self) -> None:
        assert TraceBack

    def test_context_manager(self) -> None:
        cm = TraceBack
        try:
            raise IndentationError("IndentationError")
        except IndentationError as ex:
            cm.set_Error_and_Traceback(
                str(ex),
                traceback.format_exc().split("\n"),
                traceback.format_stack(),
            )
        assert cm.error == "IndentationError"
        assert isinstance(cm.traceback, list)
        assert len(cm.traceback) > 0
        assert isinstance(cm.stack, list)
        assert len(cm.stack) > 0

    def test_context_manager_headers(self) -> None:
        TraceBack.resetValues()
        cm = TraceBack
        h: Tuple = (b"header1", b"one")
        headers: Headers = Headers(h)
        cm._getHeaders(headers)

        assert cm.headers["header1"] == h[1].decode("utf-8")

    def test_context_manager_wrong_headers(self) -> None:
        TraceBack.resetValues()
        cm = TraceBack
        h: Tuple = (b"header1", "one")
        headers: Headers = Headers(h)

        cm._getHeaders(headers)

        assert not bool(cm.headers)

    def test_context_manager_body(self) -> None:
        TraceBack.resetValues()
        cm = TraceBack
        body: bytes = b'{"key": "value"}'
        cm._getBody(body)

        assert cm.body["key"] == json.loads(body.decode("utf-8"))["key"]

    def test_context_manager_wrong_body(self) -> None:
        TraceBack.resetValues()
        cm = TraceBack
        body: Dict = {"key": "value"}

        cm._getBody(body)

        assert not bool(cm.body)

    def test_context_manager_scopes_valid(self) -> None:
        TraceBack.resetValues()
        cm = TraceBack
        scopes: Dict = {"method": "method"}
        cm._getScope(scopes)

        assert cm.scope == scopes

    def test_context_manager_scopes_inValid(self) -> None:
        TraceBack.resetValues()
        cm = TraceBack
        scopes: Dict = {"scope1": 1}
        cm._getScope(scopes)

        assert not bool(cm.scope)
