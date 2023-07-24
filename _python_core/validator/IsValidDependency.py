from typing import Any, Dict

TData = Dict[str, Any]

import _python_core.Errors as err
from _python_core.crud.crud_single import CrudOne
from _python_core.validator.validator import Validator, translate_format_from_args


class IsValidDependency(Validator):
    def __init__(self, validator: Validator):
        self.lang: str = validator.lang
        self.crud: CrudOne = validator.crud

    def validate(self, id: str, field: str) -> bool:
        if not id or id == "000000000000000000000000":
            raise err.ErrorValidatorValidDependency(
                translate_format_from_args(
                    "ERROR_INVALID_VALUE_FOR_SPECIFIC_FIELD", self.lang, field
                ),
                **{"field": field}
            )
        return True
