from typing import Any, Dict

TData = Dict[str, Any]

import _python_core.Errors as err
from _python_core.crud.crud_single import CrudOne
from _python_core.validator.validator import (
    Validator,
    translate_format_from_args,
)


class MissingField(Validator):
    def __init__(self, validator: Validator):
        self.lang: str = validator.lang
        self.crud: CrudOne = validator.crud

    def validate(self, schema: TData, field: str) -> bool:
        if field in schema:
            return False
        raise err.ErrorValidatorMissingField(
            translate_format_from_args(
                "ERROR_MISSING_FIELD",
                self.lang,
                field,
            ),
            **{"field": field}
        )
