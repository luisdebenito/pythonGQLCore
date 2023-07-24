from typing import Any, Dict

TData = Dict[str, Any]

import _python_core.Errors as err
from _python_core.validator.validator import Validator, translate


class IsEmpty(Validator):
    def __init__(self, validator: Validator):
        self.lang: str = validator.lang
        super().__init__(validator.lang)

    def validate(self, schema: TData) -> bool:
        if schema:
            return False
        raise err.ErrorValidatorEmpty(translate("ERROR_EMPTY_DATA", lang=self.lang))
