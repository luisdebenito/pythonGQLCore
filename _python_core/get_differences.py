import copy
from typing import Any, Dict, List, Optional

import _python_core.functions as fn
from _python_core import Errors as err
from _python_core.translations import Translations as tr

Object = Dict[str, Any]


class ExceptionDifferentTypes(err.ErrorBase):
    def __init__(self, field: str = "", lang: str = "en") -> None:
        self.message = translate("ERROR_TYPE_MISMATCH", lang).format(field)
        super().__init__(self.message, **{"field": field})


class GetDifferences:
    def __init__(self, lang: str = "en", *omit_fields: Any) -> None:
        self.changeLog: List = []
        self.lanf: str = lang
        self.possibleErrorField: str = ""
        self._OMIT_FIELDS = [
            "_id",
            "id",
            "createUserId",
            "createUser",
            "createDate",
            "modifiedUserId",
            "modifiedUser",
            "modifiedDate",
            "deletedUserId",
            "deletedUser",
            "deletedDate",
        ]
        self._OMIT_FIELDS.extend(omit_fields)

    def get_differences(self) -> List:
        return self.changeLog

    def calculate(self, newItem: Any, oldItem: Any) -> None:
        self.__reset()
        self.__get_differences(newItem, oldItem)

    def __reset(self) -> None:
        self.changeLog = []

    def __get_differences(self, item1: Any, item2: Any, path_key: Optional[str] = None) -> None:
        # sourcery no-metrics skip: remove-pass-elif
        """Gets differences"""

        if item1 is None or item2 is None:
            self.__get_differencesNoContainer(item1, item2, path_key)

        # Dict
        elif isinstance(item1, dict):
            self.__get_differencesDict(item1, item2, path_key)

        # List
        elif isinstance(item2, list):
            item1_diff = self.__get_differencesList(item1, item2)
            item2_diff = self.__get_differencesList(item2, item1)
            self.__setChangeLogForLists(item1_diff, item2_diff, path_key)

        # Set
        elif isinstance(item1, set):
            # Not implemente yet
            pass

        # String, Bool, Int, Float
        else:
            self.__get_differencesNoContainer(item1, item2, path_key)

    def __get_differencesDict(
        self, item1: Object, item2: Object, path_key: Optional[str] = None
    ) -> None:
        # sourcery no-metrics
        """Gets differences between dictionaries"""
        old_key: Optional[str] = ""
        # Case Intersection
        path_key = self._get_differencesDictForIntersection(item1, item2, path_key)

        # Case Difference
        # Be carefull, this logic is meant to determine ONLY if new fields are added to item2
        new_elements = set(item1).difference((set(item2)))
        for key in new_elements:
            old_key = path_key
            if key in self._OMIT_FIELDS:
                continue
            path_key = key if path_key is None else f"{path_key}.{key}"
            self.changeLog.append(
                {
                    "field": path_key,
                    "oldValue": None,
                    "newValue": str(item1[key]),
                }
            )
            path_key = old_key

        old_elements = set(item2).difference((set(item1)))
        for key in old_elements:
            old_key = path_key
            if key in self._OMIT_FIELDS and not path_key:
                continue
            path_key = key if path_key is None else f"{path_key}.{key}"
            self.changeLog.append(
                {
                    "field": path_key,
                    "oldValue": str(item2[key]),
                    "newValue": None,
                }
            )
            path_key = old_key

    def _get_differencesDictForIntersection(
        self, item1: Dict, item2: Dict, path_key: Optional[str]
    ) -> Optional[str]:  # sourcery no-metrics
        common_elements = set(item1).intersection(item2)
        for key in common_elements:
            old_key = path_key
            if key in self._OMIT_FIELDS and not path_key:
                continue
            path_key = key if path_key is None else f"{path_key}.{key}"
            self.possibleErrorField = key
            self.__get_differences(item1[key], item2[key], path_key=path_key)
            path_key = old_key
        return path_key

    def __get_differencesList(self, item1: List[Any], item2: List[Any]) -> List:
        # sourcery no-metrics
        """Gets differences between Lists or Sets"""

        diff_item1: List = copy.deepcopy(item1)
        item2_copy: List = copy.deepcopy(item2)
        for elm in item1:
            if elm in self._OMIT_FIELDS:
                diff_item1.pop(diff_item1.index(elm))
                continue

            # elm in ITEM2: same? different?
            if elm in item2:
                diff_item1.pop(diff_item1.index(elm))
                item2_copy.pop(item2_copy.index(elm))

        return diff_item1

    def __setChangeLogForLists(self, item1: Any, item2: Any, path_key: Optional[str] = "") -> None:
        if bool(item1) or bool(item2):
            self.changeLog.append(
                {
                    "field": path_key,
                    "oldValue": str(item2),
                    "newValue": str(item1),
                }
            )

    def __get_differencesNoContainer(self, item1: Any, item2: Any, name: Optional[str]) -> None:
        if fn.getHash(item1) != fn.getHash(item2):
            self.changeLog.append(
                {
                    "field": name,
                    "oldValue": str(item2),
                    "newValue": str(item1),
                }
            )


def translate(msg: str, lang: str = "en") -> str:
    return tr.translate(msg, lang)
