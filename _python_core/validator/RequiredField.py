from datetime import date, time
from operator import ne
from typing import Any, Dict

TData = Dict[str, Any]

import _python_core.Errors as err
from _python_core.crud.crud_single import CrudOne
from _python_core.validator.validator import (
    Validator,
    translate_format_from_args,
)


class RequiredField(Validator):
    def __init__(self, validator: Validator):
        self.lang: str = validator.lang
        self.crud: CrudOne = validator.crud

    def validate(self, schema: TData, field: str) -> bool:
        if (
            schema.get(field)
            or isinstance(schema.get(field), bool)
            or isinstance(schema.get(field), int)
            or isinstance(schema.get(field), float)
        ):
            return True
        raise err.ErrorValidatorRequiredField(translate_format_from_args("ERROR_REQUIRED_FIELD", self.lang, field), **{"field": field})  # fmt: skip
