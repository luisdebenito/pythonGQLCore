from typing import Any, Dict, List, Union

from _python_core.crud.crud_constants import (
    CREATE_DATE,
    CREATE_USER,
    DELETED_DATE,
    DELETED_USER,
    MODIFIED_DATE,
    MODIFIED_USER,
)
from _python_core.get_differences import GetDifferences
from _python_core.translations import Translations as tr

TData = Dict[str, Any]  # Type object as defined in GQL Schema


class CheckDuplicateField:
    def __init__(self, entry: Dict, lang: str = "en"):
        self.lang: str = lang
        self.entries: List[Dict] = []
        self.errors: List[Union[str, Dict]] = []
        self.isDuplicated: bool = False
        self.new_entry: Dict[str, Any] = entry
        self._tweak_entry()

    def _tweak_entry(self) -> None:
        if "_id" in self.new_entry:
            self.new_entry["id"] = self.new_entry["_id"]
            del self.new_entry["_id"]

    def get_errors(self) -> List[Union[Dict, str]]:
        return self.errors

    def check_for_duplicate(self, fieldsToCheck: List[str], entries: List[Dict]) -> None:
        self._check_fields_exist_in_entry(fieldsToCheck)
        for entry in entries:
            if (
                self._new_entry_has_id() and self._is_the_same_entry(entry)
            ) or self._missing_fields_to_check_in_entry(entry, fieldsToCheck):
                continue
            self._check_for_duplicate(fieldsToCheck, entry)

    def _check_for_duplicate(self, fieldsToCheck: List[str], entry: Dict) -> None:
        diff = GetDifferences(self.lang)
        diff.calculate(self.new_entry, entry)
        differences: List[Dict] = diff.get_differences()

        field_entry_pair = self._set_duplicate_field(fieldsToCheck, entry, differences)

        if len(field_entry_pair) == 0:
            self._set_error_for_entry(fieldsToCheck, entry)

    def _set_error_for_entry(self, fieldsToCheck: List[str], entry: Dict) -> None:
        self.isDuplicated = True
        self._set_error(fieldsToCheck, entry)

    def _set_error(self, fields: List[str], entry: Dict) -> None:  # type: ignore
        self.errors.append(self.translate("ERROR_DUPLICATE_ALREADY_EXIST", fields))

    def _set_duplicate_field(
        self, fieldsToCheck: List[str], entry: Dict, differences: List
    ) -> List:
        return [
            (field, entry)
            for field in fieldsToCheck
            if self._is_field_in_differences(differences, field)
        ]

    def is_duplicated(self) -> bool:
        return self.isDuplicated

    def _new_entry_has_id(self) -> bool:
        return bool(self.new_entry.get("id"))

    def _is_the_same_entry(self, entry: Dict) -> bool:
        return str(self.new_entry.get("id")) in [
            str(entry.get("_id")),
            str(entry.get("id")),
        ]

    def _missing_fields_to_check_in_entry(self, entry: Dict, fieldsToCheck: List[str]) -> bool:
        return any(field not in entry for field in fieldsToCheck)

    def _check_fields_exist_in_entry(self, fieldsToCheck: List[str]) -> None:
        for field in fieldsToCheck:
            if not bool(self.new_entry.get(field)):
                raise AssertionError(self.translate("ERROR_DUPLICATE_NON_EXISTING_FIELD", [field]))

    def _is_field_in_differences(self, differences: List[Dict], field: str) -> bool:
        # USE CASE:
        # differences_fields = ['costype.id','description']
        # field = 'costype'
        # a = any([field in diff for diff in differences_fields])

        differences_fields: List[Any] = [item.get("field") for item in differences]
        return any(field in diff for diff in differences_fields)

    def translate(self, msg: str, data: List[str] = []) -> str:
        msg = tr.translate(msg, self.lang)

        for elm in [
            CREATE_USER,
            CREATE_DATE,
            MODIFIED_USER,
            MODIFIED_DATE,
            DELETED_USER,
            DELETED_DATE,
            "id",
            "_id",
        ]:
            if elm in self.new_entry:
                del self.new_entry[elm]

        return msg.format(str(self.new_entry), ",".join(data))
