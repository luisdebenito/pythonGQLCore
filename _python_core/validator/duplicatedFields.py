from typing import Any, Dict, List, Tuple

TData = Dict[str, Any]

import _python_core.Errors as err
from _python_core.crud.crud_single import CrudOne
from _python_core.validator.validator import Validator, translate


class DuplicatedField(Validator):
    def __init__(self, validator: Validator):
        self.lang: str = validator.lang
        self.crud: CrudOne = validator.crud

    async def validate(self, fields: List[Tuple] = []) -> bool:
        if not fields:
            return False

        self._set_filter(fields)
        if not await self.crud.get(**self._filter):
            return False

        del self._filter["$or"]
        raise err.ErrorValidatorDuplicatedField(
            translate(
                "ERROR_DUPLICATE_ALREADY_EXIST", {f[0]: f[1] for f in fields}, lang=self.lang
            )
        )

    def _set_filter(self, fields: List[Tuple]) -> None:
        self._filter = {
            "$or": [
                {"projectId": self.crud.options.projectId},
                {"project.id": self.crud.options.projectId},
            ],
        }
        for elm in fields:
            self._filter[elm[0]] = elm[1]
