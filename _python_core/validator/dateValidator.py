import _python_core.Errors as err
from _python_core.crud.crud_single import CrudOne
from _python_core.validator.validator import Validator, translate
from datetime import datetime


class IsIsoFormatDate(Validator):
    def __init__(self, validator: Validator):
        self.lang: str = validator.lang
        self.crud: CrudOne = validator.crud

    def validate(self, date_text: str | datetime) -> bool:
        if isinstance(date_text, str):
            try:
                if date_text.endswith("Z"):
                    datetime.fromisoformat(date_text[:-1])
                else:
                    datetime.fromisoformat(date_text)
            except ValueError as e:
                raise err.ErrorValidatorIsIsoFormatDate(
                    translate("ERROR_DATE_FORMAT"), **{"field": "date"}
                ) from e

        return True
