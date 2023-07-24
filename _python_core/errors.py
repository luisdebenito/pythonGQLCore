from typing import Dict


class ErrorBase(Exception):
    def __init__(self, msg: str, **kwargs: Dict):
        self.message: str = msg
        self.kwargs: Dict = kwargs
        super().__init__(self.message)


class ErrorEmptyData(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorDuplicatedField(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorInvalidID(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorUniqueCode(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorAlreadyProvided(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class NonexistingData(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


# Validations
class ErrorValidatorEmpty(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorValidatorExistInDatabase(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorValidatorMissingField(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorValidatorIsAttributeUsed(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorValidatorDuplicatedField(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorMatchType(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorValidatorValidDependency(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorValidatorIsIsoFormatDate(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)


class ErrorValidatorRequiredField(ErrorBase):
    def __init__(self, msg: str, **kwargs: Dict):
        super().__init__(msg, **kwargs)
