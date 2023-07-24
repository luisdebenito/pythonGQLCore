import os
import sys
from typing import Dict, List
import pytest

from bson import ObjectId

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core import functions as fn


class TestEntryHasIDAndIsIDValid:
    def test_entryHasID_1(self) -> None:
        entry: Dict = {"id": "616c1656f29b947922fe7a40"}
        assert fn.entryHasIDNoNull(entry)

    def test_entryHasID_2(self) -> None:
        entry: Dict = {"_id": "616c1656f29b947922fe7a40"}
        assert fn.entryHasIDNoNull(entry)

    def test_entryHasID_3(self) -> None:
        entry: Dict = {"_id": "616c1656f29b97922fe7a40"}
        assert fn.entryHasIDNoNull(entry)

    def test_entryHasID_4(self) -> None:
        entry: Dict = {"_id": ""}
        assert fn.entryHasIDNoNull(entry) is False

    def test_entryHasID_5(self) -> None:
        entry: Dict = {}
        assert fn.entryHasIDNoNull(entry) is False

    def test_isValidID_1(self) -> None:
        entry: Dict = {"id": ObjectId("616c1656f29b947922fe7a40")}
        assert fn.isValidID(entry)

    def test_isValidID_2(self) -> None:
        entry: Dict = {"_id": ObjectId("616c1656f29b947922fe7a40")}
        assert fn.isValidID(entry)

    def test_isValidID_3(self) -> None:
        entry: Dict = {"id": ""}
        assert fn.isValidID(entry) is False

    def test_isValidID_4(self) -> None:
        entry: Dict = {}
        assert fn.isValidID(entry) is False

    def test_isValidID_5(self) -> None:
        entry: Dict = {"id": 4}
        assert fn.isValidID(entry) is False

    # prettier-ignore
    def test_find_type_in_schema_code_CostCode(self) -> None:
        assert (
            fn.find_type_in_schema(
                "CostCode",
                f"{os.path.dirname(__file__)}/test_file_find_type_in_schema.txt",
                "code",
            )
            == "str"
        )

    def test_find_type_in_schema_description_CostCode(self) -> None:
        assert (
            fn.find_type_in_schema(
                "CostCode",
                f"{os.path.dirname(__file__)}/test_file_find_type_in_schema.txt",
                "description",
            )
            == "str"
        )

    def test_no_classname_find_type_in_schema(self) -> None:
        assert (
            fn.find_type_in_schema(
                "", f"{os.path.dirname(__file__)}/test_file_find_type_in_schema.txt", "description"
            )
            is None
        )

    def test_not_found_exists_find_type_in_schema(self) -> None:
        with pytest.raises(FileNotFoundError):
            fn.find_type_in_schema(
                "CostCode", f"{os.path.dirname(__file__)}/test_file_non_exists.txt", "description"
            )

    def test_no_field_find_type_in_schema(self) -> None:
        assert (
            fn.find_type_in_schema(
                "CostCode", f"{os.path.dirname(__file__)}/test_file_find_type_in_schema.txt", ""
            )
            is None
        )

    def test_no_match_field_find_type_in_schema(self) -> None:
        assert (
            fn.find_type_in_schema(
                "CostCode",
                f"{os.path.dirname(__file__)}/test_file_find_type_in_schema.txt",
                "codeTest",
            )
            is None
        )

    def test_no_match_classname_find_type_in_schema_description_CostCode(self) -> None:
        assert (
            fn.find_type_in_schema(
                "CostCodeTEST",
                f"{os.path.dirname(__file__)}/test_file_find_type_in_schema.txt",
                "code",
            )
            is None
        )

    def test_transform_list_dict_to_list_tuple(self) -> None:
        entry: List[Dict] = [{"key1": "asc"}]
        assert fn.transform_list_dict_to_list_tuple(entry) == [("key1", 1)]
