from typing import Any, Dict, List, Union

from bson import ObjectId
from pymongo import MongoClient

from _python_core import Errors as err
from _python_core.crud.crud import Crud, ErrorCRUD
from _python_core.crud.crud_options import CrudOptions
from _python_core.crud.crud_single import CrudOne
from _python_core.http_codes import HTTPCode
from _python_core.translations import Translations as tr

TData = Dict[str, Any]  # Type object as defined in GQL Schema
TMessages = List[str]
TInsertedData = List[TData]


class CrudMany(Crud):
    def __init__(self, mongo: MongoClient, lang: str = "en") -> None:
        super().__init__(mongo, lang)
        self._initialize_values(mongo, lang)

    def _initialize_values(self, mongo: Any, lang: str) -> None:
        self.crud: CrudOne = CrudOne(mongo, lang)
        self.crud.set_options(self.options)
        self.schemas: List[TData] = []
        self.messages: List[str] = []
        self.errors: List[str] = []
        self.data: List[TData] = []
        self.http_codes: List[int] = []

    def set_options(self, options: CrudOptions) -> None:
        self.options = options
        self.crud.options = options
        self._verifyLanguage()

    def set_language(self, lang: str) -> None:
        self.lang = lang
        self.options.lang = lang
        self.crud.lang = lang
        self.crud.options.lang = lang

    def set_collection(self, collection: str) -> None:
        self.collection = collection
        self.mongo = self.mongoDB[self.collection]
        self.crud.set_collection(collection)

    def set_softDelete(self, softDelete: bool = True) -> None:
        self.options.softDelete = softDelete
        self.crud.options.softDelete = softDelete

    def request_postprocess(func: Any) -> Any:
        async def wrapped(  # type: ignore
            crud: Crud, data: List[Union[str, Dict]], *args: Any, **kwargs: Dict
        ) -> Dict:  # sourcery skip: raise-specific-error
            try:
                await func(crud, data, *args, **kwargs)
            except (err.ErrorBase, AssertionError) as excinfo:
                raise err.ErrorBase(str(excinfo)) from excinfo
            except Exception as excinfo:
                raise Exception(str(excinfo)) from excinfo
            finally:
                crud.postprocess()

        return wrapped

    def postprocess(self) -> None:
        self.schemas = []
        self._set_http_code_in_postprocessing()

    def _set_http_code_in_postprocessing(self) -> None:
        if not bool(self.http_code):  # type: ignore
            self.http_code = (
                self.http_codes[0]
                if self._have_all_children_the_same_http_code()
                else HTTPCode.CODE_400
            )

    def _have_all_children_the_same_http_code(self) -> bool:
        return all(
            [
                bool(self.http_codes),
                self.http_codes.count(self.http_codes[0]) == len(self.http_codes),
            ]
        )

    @request_postprocess
    async def insert_update(self, schemas: List[TData]) -> None:
        self.schemas = schemas
        self._reset_messages_errors_http_codes_and_data()
        if self._is_empty_data():
            return

        await self._process_schema_insert_update()

    def _is_empty_data(self) -> bool:
        if not bool(self.schemas):
            self._set_error("ERROR_EMPTY_SCHEMA", HTTPCode.CODE_400)
            return True

        return False

    def _set_error(self, msg: str, http_code: HTTPCode = HTTPCode.CODE_400) -> None:
        self.errors.append(self.translate(msg))
        self.http_code = http_code.value

    async def _process_schema_insert_update(self) -> None:
        for schema in self.schemas:
            try:
                await self.crud.insert_update(schema)
                self._transfer_information_to_parent()
            except (AssertionError, ErrorCRUD):
                self._set_error_from_children()
            except Exception as err:
                self.errors.append(str(err))
                self._set_error_from_children()

    def _transfer_information_to_parent(self) -> None:
        self.messages.append(self.crud.get_message())
        self.data.append(self.crud.get_data())
        self.http_codes.append(self.crud.get_http_code())

    def _set_error_from_children(self) -> None:
        self.errors.append(self.crud.get_error())
        self.http_codes.append(self.crud.get_http_code())

    @request_postprocess
    async def delete(self, ids: List[str]) -> None:  # type: ignore
        self.schemas = [{"_id": ObjectId(id)} for id in ids]
        self._reset_messages_errors_http_codes_and_data()
        if self._is_empty_data():
            return

        await self._process_schema_delete()

    async def _process_schema_delete(self) -> None:
        for schema in self.schemas:
            try:
                await self.crud.delete(str(schema["_id"]))
                self._transfer_information_to_parent()
            except (AssertionError, ErrorCRUD):
                self._set_error_from_children()
            except Exception as err:
                self.errors.append(str(err))
                self._set_error_from_children()

    def _reset_messages_errors_http_codes_and_data(self) -> None:
        self._reset_messages()
        self._reset_data()
        self._reset_errors()
        self._reset_http_codes()
        self._reset_http_code()

    def _reset_messages(self) -> None:
        self.messages = []

    def _reset_errors(self) -> None:
        self.errors = []

    def _reset_data(self) -> None:
        self.data = []

    def _reset_http_codes(self) -> None:
        self.http_codes = []

    def _reset_http_code(self) -> None:
        self.http_code = None

    def get_messages(self) -> List[str]:
        return self.messages

    def get_errors(self) -> List[str]:
        return self.errors

    def get_data(self) -> List[TData]:
        return self.data

    def get_http_code(self) -> HTTPCode:
        return self.http_code

    def translate(self, msg: str) -> str:
        return tr.translate(msg)
