import os
import sys

import pytest

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.checkDuplicate import CheckDuplicateField as cf


class TestCheckDuplicate_Bulk_without_id:
    bulkUpload = True
    entry = {"one": 1}
    index: int = 3
    my_class = cf(entry)

    def test_create_class(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        assert self.my_class.entries == []
        assert self.my_class.new_entry == self.entry

    def test_create_class_fieldToCheck_not_in_entry(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        with pytest.raises(AssertionError) as excinfo:
            self.my_class.check_for_duplicate(["two"], [])

        assert self.my_class.translate("ERROR_DUPLICATE_NON_EXISTING_FIELD", ["two"]) == str(
            excinfo.value
        )

    def test_create_class_fieldToCheck_not_in_entries(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is False
        assert len(self.my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_1(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"one": 2}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is False
        assert len(self.my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_2(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"id": "1", "one": 1}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 1

    def test_check_fieldToCheck_in_entries_with_different_value_3(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"id": "11", "one": 1}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 1

    def test_check_field_in_entries_same_value_1(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"one": 1}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 1


class TestCheckDuplicate_Bulk_with_id:
    bulkUpload = True
    entry = {"id": "1", "one": 1}
    index: int = 3

    def test_create_class(self) -> None:
        my_class = cf(self.entry)
        assert my_class.entries == []
        assert my_class.new_entry == self.entry

    def test_create_class_fieldToCheck_not_in_entry(self) -> None:
        my_class = cf(self.entry)
        with pytest.raises(AssertionError) as excinfo:
            my_class.check_for_duplicate(["two"], [])

        assert my_class.translate("ERROR_DUPLICATE_NON_EXISTING_FIELD", ["two"]) == str(
            excinfo.value
        )

    def test_create_class_fieldToCheck_not_in_entries(self) -> None:
        my_class = cf(self.entry)
        entries = [{"three": 3}, {"four": 4}]
        my_class.check_for_duplicate(["one"], entries)

        assert my_class.is_duplicated() is False
        assert len(my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_1(self) -> None:
        # sourcery skip: class-extract-method
        my_class = cf(self.entry)
        entries = [{"one": 2}, {"three": 3}, {"four": 4}]
        my_class.check_for_duplicate(["one"], entries)

        assert my_class.is_duplicated() is False
        assert len(my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_2(self) -> None:
        # sourcery skip: class-extract-method
        my_class = cf(self.entry)
        entries = [{"id": "2", "one": 11}, {"three": 3}, {"four": 4}]
        my_class.check_for_duplicate(["one"], entries)

        assert my_class.is_duplicated() is False
        assert len(my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_3(self) -> None:
        # sourcery no-metrics skip: class-extract-method
        my_class = cf(self.entry)
        entries = [{"id": "11", "one": 1}, {"three": 3}, {"four": 4}]
        my_class.check_for_duplicate(["one"], entries)

        assert my_class.is_duplicated() is True
        assert len(my_class.get_errors()) == 1

    def test_check_field_in_entries_same_value_1(self) -> None:
        my_class = cf(self.entry)
        entries = [{"one": 1}, {"three": 3}, {"four": 4}]
        my_class.check_for_duplicate(["one"], entries)

        assert my_class.is_duplicated() is True
        assert len(my_class.get_errors()) == 1


class TestCheckDuplicate_noBulk_entry_with_id:
    bulkUpload = False
    entry = {"_id": "1", "one": 1}
    my_class = cf(entry)

    def test_create_class(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        assert self.my_class.entries == []
        assert self.my_class.new_entry == self.entry

    def test_create_class_fieldToCheck_not_in_entry(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        with pytest.raises(AssertionError) as excinfo:
            self.my_class.check_for_duplicate(["two"], [])

        assert self.my_class.translate("ERROR_DUPLICATE_NON_EXISTING_FIELD", ["two"]) == str(
            excinfo.value
        )

    def test_create_class_fieldToCheck_not_in_entries(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is False
        assert len(self.my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_1(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"one": 2}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is False
        assert len(self.my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_2(self) -> None:
        # sourcery skip: class-extract-method
        my_class = cf(self.entry)
        entries = [{"id": "2", "one": 11}, {"three": 3}, {"four": 4}]
        my_class.check_for_duplicate(["one"], entries)

        assert my_class.is_duplicated() is False
        assert len(my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_3(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"id": "11", "one": 1}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 1
        assert (
            self.my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one"])
            == self.my_class.get_errors()[0]
        )

    def test_check_field_in_entries_same_value_1(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"one": 1}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 1
        assert (
            self.my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one"])
            == self.my_class.get_errors()[0]
        )


class TestCheckDuplicate_noBulk_entry_without_id:
    bulkUpload = False
    entry = {"one": 1}
    my_class = cf(entry)

    def test_create_class(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        assert self.my_class.entries == []
        assert self.my_class.new_entry == self.entry

    def test_create_class_fieldToCheck_not_in_entry(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        with pytest.raises(AssertionError) as excinfo:
            self.my_class.check_for_duplicate(["two"], [])

        assert self.my_class.translate("ERROR_DUPLICATE_NON_EXISTING_FIELD", ["two"]) == str(
            excinfo.value
        )

    def test_create_class_fieldToCheck_not_in_entries(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is False
        assert len(self.my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_1(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"one": 2}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is False
        assert len(self.my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_2(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"id": "1", "one": 1}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 1
        assert (
            self.my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one"])
            == self.my_class.get_errors()[0]
        )

    def test_check_fieldToCheck_in_entries_with_different_value_3(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"id": "11", "one": 1}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 1
        assert (
            self.my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one"])
            == self.my_class.get_errors()[0]
        )

    def test_check_field_in_entries_same_value_1(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"one": 1}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 1
        assert (
            self.my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one"])
            == self.my_class.get_errors()[0]
        )


class TestCheckDuplicate_noBulk_entry_without_id_MultipleFields:
    bulkUpload = False
    entry = {"one": 1, "two": 2}
    my_class = cf(entry)

    def test_create_class(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        assert self.my_class.entries == []
        assert self.my_class.new_entry == self.entry

    def test_create_class_fieldToCheck_not_in_entries_1(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one", "two"], entries)

        assert self.my_class.is_duplicated() is False
        assert len(self.my_class.get_errors()) == 0

    def test_create_class_fieldToCheck_not_in_entries_2(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"two": 2, "three": 3}, {"one": 3, "four": 4}]
        self.my_class.check_for_duplicate(["one", "two"], entries)

        assert self.my_class.is_duplicated() is False
        assert len(self.my_class.get_errors()) == 0

    def test_create_class_fieldToCheck_not_in_entries_3(self) -> None:
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"two": 2, "three": 3}, {"one": 1, "four": 4}]
        self.my_class.check_for_duplicate(["one", "two"], entries)

        assert self.my_class.is_duplicated() is False
        assert len(self.my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_1(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"one": 2, "two": 2}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one", "two"], entries)

        assert self.my_class.is_duplicated() is False
        assert len(self.my_class.get_errors()) == 0

    def test_check_fieldToCheck_in_entries_with_different_value_2(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"id": "1", "one": 1, "two": 2}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one", "two"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 1
        assert (
            self.my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one", "two"])
            == self.my_class.get_errors()[0]
        )

    def test_check_fieldToCheck_in_entries_with_different_value_3(self) -> None:
        # sourcery skip: class-extract-method
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [{"id": "11", "one": 1, "two": 2}, {"three": 3}, {"four": 4}]
        self.my_class.check_for_duplicate(["one", "two"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 1
        assert (
            self.my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one", "two"])
            == self.my_class.get_errors()[0]
        )

    def test_check_field_in_entries_same_value_1(self) -> None:
        # sourcery no-metrics
        self.my_class.isDuplicated = False
        self.my_class.errors = []
        entries = [
            {"one": 1, "two": 2},
            {"three": 3, "one": 1, "two": 2},
            {"four": 4, "one": 1, "two": 2},
        ]
        self.my_class.check_for_duplicate(["one", "two"], entries)

        assert self.my_class.is_duplicated() is True
        assert len(self.my_class.get_errors()) == 3
        assert (
            self.my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one", "two"])
            == self.my_class.get_errors()[0]
        )
        assert (
            self.my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one", "two"])
            == self.my_class.get_errors()[1]
        )
        assert (
            self.my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one", "two"])
            == self.my_class.get_errors()[2]
        )

    def test_check_field_in_entries_with_3_fields_to_check(self) -> None:
        # sourcery no-metrics
        entry = {"one": 1, "two": 2, "three": 3}
        my_class = cf(entry)
        entries = [
            {"one": 1, "two": 2, "three": 3},
            {"three": 3, "one": 1, "two": 2},
            {"four": 4, "one": 1, "two": 2},
        ]
        my_class.check_for_duplicate(["one", "two", "three"], entries)

        assert my_class.is_duplicated() is True
        assert len(my_class.get_errors()) == 2
        assert (
            my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one", "two", "three"])
            == my_class.get_errors()[0]
        )
        assert (
            my_class.translate("ERROR_DUPLICATE_ALREADY_EXIST", ["one", "two", "three"])
            == my_class.get_errors()[1]
        )
