import os
import sys
from typing import Any, Dict, List, Set

import pytest

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.get_differences import GetDifferences, ExceptionDifferentTypes
from _python_core.translations import Translations as tr


class GetDifferencesHelper:
    lang: str = "en"
    diff = GetDifferences(lang=lang)

    def assertDiff(self, item1: Any, item2: Any, isDifferent: bool, length: int = None) -> None:
        self.diff.calculate(item1, item2)
        assert bool(self.diff.get_differences()) is isDifferent

        if length:
            assert len(self.diff.get_differences()) == length

    def assert_history(self, changelog: List, field: str, oldValue: Any, newValue: Any) -> None:
        for item in changelog:
            if item["field"] == field:
                assert item["field"] == field
                assert item["oldValue"] == oldValue
                assert item["newValue"] == newValue
                return


class TestGetDifferences_simple_types(GetDifferencesHelper):
    def test_no_matching_type_but_valid_with_None(self) -> None:
        self.diff.calculate(None, 3)
        assert bool(self.diff.get_differences())

    def test_simple_int(self) -> None:
        self.assertDiff(3, 2, True)
        self.assertDiff(2, 2, False)

    def test_simple_string(self) -> None:
        self.assertDiff("hello", "world", True)
        self.assertDiff("hello", "hello", False)
        self.assertDiff("hello", "hello ", True)

    # @pytest.mark.skip
    def test_simple_float(self) -> None:
        self.assertDiff(2.0, 3.0, True)
        self.assertDiff(2.0, 2.0, False)

    def test_simple_bool(self) -> None:
        self.assertDiff(False, False, False)
        self.assertDiff(False, True, True)


class TestGetDifferences_dict(GetDifferencesHelper):
    def test_simple_dict(self) -> None:
        a: Dict = {"uno": 1}
        b: Dict = {"uno": 1}
        self.assertDiff(a, b, False)
        c: Dict = {"uno": 2}
        self.assertDiff(a, c, True, 1)
        self.assert_history(self.diff.changeLog, "uno", "2", "1")

    def test_simple_id_with_no_path(self) -> None:
        a: Dict = {"id": 1}
        b: Dict = {"id": 2}
        self.assertDiff(a, b, False)

    def test_simple_id_with_path(self) -> None:
        a: Dict = {"class": {"id": 1}}
        b: Dict = {"class": {"id": 2}}
        self.assertDiff(a, b, True)

    def test_complex_dict1(self) -> None:
        a: Dict = {"uno": 1, "dos": 2}
        b: Dict = {"uno": 1, "tres": 3}
        self.assertDiff(a, b, True, 2)
        self.assert_history(self.diff.changeLog, "dos", None, "2")
        self.assert_history(self.diff.changeLog, "tres", "3", None)

    def test_complex_dict2(self) -> None:
        a: Dict = {"uno": 1, "dos": 2, "cuatro": 4}
        b: Dict = {"uno": 1, "tres": 3, "cuatro": 0}

        self.assertDiff(a, b, True, 3)
        self.assert_history(self.diff.changeLog, "cuatro", "0", "4")
        self.assert_history(self.diff.changeLog, "dos", None, "2")
        self.assert_history(self.diff.changeLog, "tres", "3", None)

    def test_complex_dict3(self) -> None:
        a: Dict = {"uno": 1, "uno_bis": {"dos": 2}}
        b: Dict = {"uno": 1, "uno_bis": {"dos": 0}}
        self.assertDiff(a, b, True, 1)
        self.assert_history(self.diff.changeLog, "uno_bis.dos", "0", "2")

    def test_complex_dict4(self) -> None:
        a: Dict = {"uno": 1, "uno_bis": {"dos": 2, "tres": 0}}
        b: Dict = {"uno": 1, "uno_bis": {"dos": 2, "tres": 3}}
        self.assertDiff(a, b, True, 1)
        self.assert_history(self.diff.changeLog, "uno_bis.tres", "3", "0")

    def test_complex_dict5(self) -> None:
        # sourcery no-metrics
        a: Dict = {"uno": 1, "uno_bis": {"dos": 2, "tres": 0}}
        b: Dict = {"uno": 1, "uno_bis": {"dos": 0, "tres": 3}}
        self.assertDiff(a, b, True, 2)
        self.assert_history(self.diff.changeLog, "uno_bis.dos", "0", "2")
        self.assert_history(self.diff.changeLog, "uno_bis.tres", "3", "0")

    def test_complex_dict6(self) -> None:  # sourcery no-metrics
        a: Dict = {
            "uno": 1,
            "uno_bis": {
                "dos": 2,
                "dos_bis": {"tres": 3, "cuatro": 4, "cinco": 5},
            },
        }
        b: Dict = {
            "uno": 0,
            "uno_bis": {
                "dos": 0,
                "dos_bis": {"tres": 3, "cuatro": 0, "seis": 6},
            },
        }

        self.assertDiff(a, b, True, 5)
        self.assert_history(self.diff.changeLog, "uno", "0", "1")
        self.assert_history(self.diff.changeLog, "uno_bis.dos", "0", "2")
        self.assert_history(self.diff.changeLog, "uno_bis.dos_bis.cinco", None, "5")
        self.assert_history(self.diff.changeLog, "uno_bis.dos_bis.cuatro", "0", "4")
        self.assert_history(self.diff.changeLog, "uno_bis.dos_bis.seis", "6", None)

    def test_complex_dict7(self) -> None:
        # sourcery no-metrics
        a: Dict = {
            "uno": 1,
            "uno_bis": {
                "dos": 2,
                "dos_bis": {"cuatro": 4},
                "siete": 7,
            },
            "ocho": 8,
        }
        b: Dict = {
            "uno": 1,
            "uno_bis": {
                "dos": 2,
                "dos_bis": {"cuatro": 0},
                "siete": 0,
            },
            "ocho": 10,
        }

        self.assertDiff(a, b, True, 3)
        self.assert_history(self.diff.changeLog, "uno_bis.dos_bis.cuatro", "0", "4")
        self.assert_history(self.diff.changeLog, "uno_bis.siete", "0", "7")
        self.assert_history(self.diff.changeLog, "ocho", "10", "8")


class TestGetDifferences_list(GetDifferencesHelper):
    def test_simple_list1(self) -> None:
        a: List = []
        b: List = []

        self.assertDiff(a, b, False)

    def test_simple_list2(self) -> None:
        a: List = [3]
        b: List = []

        self.assertDiff(a, b, True, 1)
        self.assert_history(self.diff.changeLog, "", str(b), str(a))

    def test_simple_list3(self) -> None:
        a: List = ["labor", "equipment"]
        b: List = ["labor", "equipment"]

        self.assertDiff(a, b, False, 0)
        self.assert_history(self.diff.changeLog, "", str(b), str(a))


class TestGetDifferences_dict_with_lists(GetDifferencesHelper):
    def test_complex_struct1(self) -> None:
        a: Dict = {"a": [3]}
        b: Dict = {"a": []}

        self.assertDiff(a, b, True, 1)
        self.assert_history(self.diff.changeLog, "a", "[]", "[3]")

    def test_complex_struct2(self) -> None:
        a: Dict = {"a": {"b": [{"cinco": 5}, 4]}}
        b: Dict = {"a": {"b": [{"cinco": 5}]}}

        self.assertDiff(a, b, True, 1)
        self.assert_history(self.diff.changeLog, "a.b", "[]", "[4]")

    def test_complex_struct3(self) -> None:
        # sourcery no-metrics
        a: Dict = {
            "a": {
                "b": [{"cinco": 5}, 4],
                "c": {"d": {"e": 4, "f": {"g": ["h", "i"]}}},
            },
        }
        b: Dict = {
            "a": {
                "b": [4],
                "c": {"d": {"e": 4, "f": {"g": ["h"]}}},
            }
        }

        self.assertDiff(a, b, True, 2)
        self.assert_history(self.diff.changeLog, "a.b", "[]", "[{'cinco': 5}]")
        self.assert_history(self.diff.changeLog, "a.c.d.f.g", "[]", "['i']")


class TestGetDifferences_sets(GetDifferencesHelper):
    def test_when_set(self) -> None:
        """Test set"""
        a: Set = {1, 2}
        b: Set = {1, 2}

        self.assertDiff(a, b, False)


class TestGetDifferences_omit_fields(GetDifferencesHelper):
    def test_omit_field_in_List_only_omit(self) -> None:
        omit_fields = ["omit"]
        a: List = ["omit"]
        b: List = ["omit"]

        self.diff = GetDifferences(*omit_fields)
        self.assertDiff(a, b, False)

    def test_omit_field_in_List_common_and_ommit(self) -> None:
        omit_fields = ["omit"]
        b = ["one", "common", "omit"]
        a = ["two", "common", "omit"]

        self.diff = GetDifferences(*omit_fields)
        self.assertDiff(a, b, True, 1)
        self.assert_history(self.diff.changeLog, "", ["two"], ["one"])


class TestErrorDifferentTypes(GetDifferencesHelper):
    def test_error_DifferentTypes(self) -> None:
        with pytest.raises(ExceptionDifferentTypes):
            raise ExceptionDifferentTypes("Error")
