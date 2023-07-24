from typing import Any, Dict

TData = Dict[str, Any]

import _python_core.Errors as err
from _python_core.crud.crud_single import CrudOne
from _python_core.validator.validator import Validator, translate_format_from_args


class MatchType(Validator):
    def __init__(self, validator: Validator):
        self.lang: str = validator.lang
        self.crud: CrudOne = validator.crud

    def validate(self, type_to_check: Any, expected_type: Any, field: str) -> bool:
        if type(type_to_check).__name__ == expected_type or (
            type(type_to_check).__name__ == "int" and expected_type == "float"
        ):
            return True

        raise err.ErrorMatchType(
            translate_format_from_args(
                "ERROR_TYPE_FIELD",
                self.lang,
                expected_type,
                str(type(type_to_check).__name__),
                field,
            ),
            **{"field": field}
        )
