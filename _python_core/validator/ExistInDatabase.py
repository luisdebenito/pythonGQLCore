from typing import Any, Dict

TData = Dict[str, Any]

import _python_core.Errors as err
from _python_core.crud.crud_single import CrudOne
from _python_core.validator.validator import Validator, translate


class ExistInDatabase(Validator):
    def __init__(self, validator: Validator):
        self.lang: str = validator.lang
        self.crud: CrudOne = validator.crud

    async def validate(self, data_id: str) -> bool:
        if await self.crud.get_by_id(data_id):
            return True
        raise err.ErrorValidatorExistInDatabase(
            translate("ERROR_DELETE_NONEXISTING", lang=self.lang)
        )
