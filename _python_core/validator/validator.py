from typing import Any, Dict

from pymongo.database import Database

from _python_core.crud.crud_options import CrudOptions
from _python_core.crud.crud_single import CrudOne

TData = Dict[str, Any]

from _python_core.crud.crud_constants import (
    CREATE_DATE,
    CREATE_USER,
    DELETED_DATE,
    DELETED_USER,
    MODIFIED_DATE,
    MODIFIED_USER,
)
from _python_core.translations import Translations as tr


class Validator:
    def __init__(self, lang: str = "en") -> None:
        self.lang: str = lang

    def set_crud(self, ddbb: Database) -> None:
        self.crud: CrudOne = CrudOne(ddbb, self.lang)
        self.crud.mongo = ddbb

    def set_crud_options(self, crudOptions: CrudOptions) -> None:
        self.crud.options = crudOptions

    def set_collection(self, collection: str) -> None:
        self.crud.collection = collection
        self.crud.mongo = self.crud.mongoDB[collection]


def translate(msg: str, data: Dict = None, lang: str = "en") -> str:
    msg = tr.translate(msg, lang)
    if not bool(data):
        return msg

    for elm in [
        CREATE_USER,
        CREATE_DATE,
        MODIFIED_USER,
        MODIFIED_DATE,
        DELETED_USER,
        DELETED_DATE,
        "id",
        "_id",
    ]:
        if elm in data:  # type: ignore
            del data[elm]  # type: ignore
    return msg.format(data)


def translate_format_from_args(msg: str, lang: str = "en", *args: Any) -> str:
    msg = tr.translate(msg, lang)
    return msg.format(*args)
