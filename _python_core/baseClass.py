import copy
from abc import ABC, abstractmethod
from typing import Any, Collection, Dict, List, Optional, Tuple, Union

from bson.objectid import ObjectId

from _python_core import functions as fn
from _python_core import Errors as err
from _python_core.ariadne_dataloader import AriadneDataLoader
from _python_core.crud.crud_constants import (
    CREATE_DATE,
    CREATE_USER,
    DELETED_DATE,
    DELETED_USER,
    MODIFIED_DATE,
    MODIFIED_USER,
)
from _python_core.crud.crud_many import CrudMany
from _python_core.crud.crud_options import CrudOptions
from _python_core.crud.crud_single import CrudOne
from _python_core.http_codes import HTTPCode
from _python_core.responseGQL import ResponseGQL
from _python_core.translations import Translations as tr
from _python_core.validator.validator import Validator

TData = Dict[str, Any]  # Type object as defined in GQL Schema


class Base(ABC):
    collection: str

    def __init__(self, **kwargs: Dict) -> None:
        self.lang: Collection[str] = kwargs["lang"] if kwargs.get("lang") else "en"
        self.bulkUpload: bool = False
        self.kwargs: Dict = kwargs

    @abstractmethod
    def set_crud(self, ddbb: Any) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def set_crud_options(self, options: CrudOptions) -> None:
        pass  # pragma: no cover

    @abstractmethod
    async def get_all(self, **filter: Dict) -> List[TData]:
        pass  # pragma: no cover

    @abstractmethod
    async def get_single(self, **filter: Any) -> TData:
        pass  # pragma: no cover

    @abstractmethod
    async def get_by_id(self, id: Union[str, ObjectId], **filter: Any) -> TData:
        pass  # pragma: no cover

    @abstractmethod
    async def get_with_limit(self, limit: int = 1, sort: List[Tuple] = [], **filter: Any) -> TData:
        pass  # pragma: no cover

    @abstractmethod
    def translate(self, msg: str) -> str:
        pass  # pragma: no cover

    @abstractmethod
    async def validate_to_insertUpdate(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    async def validate_to_delete(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    async def insert_update(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    async def insert_update_after_validation(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    async def delete(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    async def delete_after_validation(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def reset_errors(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def set_language(self, lang: str) -> None:
        pass  # pragma: no cover

    def set_bulk_upload(self, bulkUpload: bool) -> None:
        self.bulkUpload = bulkUpload

    def _is_bulk_upload(self) -> bool:
        return self.bulkUpload

    @abstractmethod
    def return_mutation(self) -> ResponseGQL:
        pass  # pragma: no cover


class BaseMany(Base):
    def __init__(self, **kwargs: Dict) -> None:
        Base.__init__(self, **kwargs)
        self._set_initialize_values()
        self.kwargs: Dict = kwargs

    def _set_initialize_values(self) -> None:
        self.errors: List[str] = []
        self.messages: List[str] = []
        self.data: List[TData] = []

        self.schemas: List[TData] = []
        self.validSchemas: List[TData] = []
        self.inValidSchemas: List[TData] = []
        self.ids: List[str] = []

    def translate(self, msg: str) -> str:
        return tr.translate(msg, self.lang)

    def return_mutation(self) -> ResponseGQL:
        return ResponseGQL(
            self.get_http_code(), self.get_messages(), self.get_errors(), self.get_data()
        )

    def set_language(self, lang: str) -> None:
        self.lang = lang
        if hasattr(self, "handlerCrudMany"):
            self.handlerCrudMany.set_language(lang)

    def set_crud(self, ddbb: Any, crudOptions: CrudOptions = None) -> None:
        self.handlerCrudMany: CrudMany = CrudMany(ddbb, self.lang)
        self.handlerCrudMany.set_collection(self.collection)
        self.handlerCrudMany.set_language(self.lang)

        if crudOptions:
            self.set_crud_options(crudOptions)

    def set_crud_options(self, options: CrudOptions) -> None:
        options.set_language(self.lang)
        self.handlerCrudMany.set_options(options)

    @abstractmethod
    def set_schemas(self, entries: List[TData]) -> None:
        pass  # pragma: no cover

    async def get_all(self, **filter: Dict) -> List[TData]:
        return await self.handlerCrudMany.get(**filter)

    async def get_single(self, sort: List[Tuple] = [], **filter: Any) -> TData:
        return await self.handlerCrudMany.get_single(sort, **filter)

    async def get_by_id(self, id: Union[str, ObjectId], **filter: Any) -> TData:
        return await self.handlerCrudMany.get_by_id(id, **filter)

    async def get_with_limit(self, limit: int = 1, sort: List[Tuple] = [], **filter: Any) -> TData:
        return await self.handlerCrudMany.get_with_limit(limit, *sort, **filter)

    def get_errors(self) -> List:
        return self.errors + (
            self.handlerCrudMany.get_errors() if hasattr(self, "handlerCrudMany") else []
        )

    def get_messages(self) -> List:
        return self.messages + (
            self.handlerCrudMany.get_messages() if hasattr(self, "handlerCrudMany") else []
        )

    def get_data(self) -> List:
        return self.data + (
            self.handlerCrudMany.get_data() if hasattr(self, "handlerCrudMany") else []
        )

    def get_http_code(self) -> TData:
        if hasattr(self, "http_code"):
            return self.http_code

        if not len(self.inValidSchemas) and len(self.validSchemas) != 0:
            return HTTPCode.CODE_200
        elif len(self.inValidSchemas) != 0 and not len(self.validSchemas):
            return HTTPCode.CODE_400
        elif len(self.inValidSchemas) != 0 and len(self.validSchemas) != 0:
            return HTTPCode.CODE_400
        elif len(self.errors):
            return HTTPCode.CODE_500
        else:
            return HTTPCode.CODE_200

    # Public method. Entry point for Insert or Delete
    async def insert_update(self) -> None:
        self.reset_errors()
        if self._are_schemas_empty():
            return
        await self.validate_to_insertUpdate()
        await self.insert_update_after_validation(only_valid=True)

    def _are_schemas_empty(self) -> bool:
        if len(self.schemas) != 0:
            return False

        self.errors.append(self.translate("ERROR_EMPTY_DATA"))
        self.inValidSchemas.extend(self.schemas)
        self.http_code = HTTPCode.CODE_400
        return True

    async def insert_update_after_validation(self, only_valid: bool = True) -> None:
        entries: List[TData] = self.validSchemas if only_valid else self.schemas
        if entries and not (self._is_bulk_upload() and len(self.inValidSchemas) > 0):
            await self.handlerCrudMany.insert_update(entries)

    async def delete(self) -> None:
        self.reset_errors()
        if self._are_ids_empty():
            return
        await self.validate_to_delete()
        await self.delete_after_validation()

    def _are_ids_empty(self) -> bool:
        if len(self.ids) != 0:
            return False

        self.errors.append(self.translate("ERROR_EMPTY_DATA"))
        self.http_code = HTTPCode.CODE_400
        return True

    async def are_there_data_to_delete(self) -> bool:
        return len(self.validSchemas) > 0

    async def delete_after_validation(self, only_valid: bool = True) -> None:
        entries: List[TData] = self.validSchemas if only_valid else self.schemas
        if entries:
            ids = [str(entry.get("_id")) for entry in entries]
            await self.handlerCrudMany.delete(ids)

    def reset_errors(self) -> None:
        self.errors = []

    def set_bulk_error(self, column: str, row: int, msg: str) -> None:
        self.errors.append(str({"column": column, "row": row, "msg": msg}))


class BaseOne(Base):
    def __init__(self, **kwargs: Dict) -> None:
        Base.__init__(self, **kwargs)
        self._set_initialize_values()
        self.kwargs: Any = kwargs
        self.validator = Validator(self.lang)

    def _set_initialize_values(self) -> None:
        self.schema: TData = {}
        self.message: str = ""
        self.error: Union[str, Dict[str, str]] = {}
        self.data: TData = {}
        self.httpCode: HTTPCode = HTTPCode.CODE_500

    def set_language(self, lang: str) -> None:
        self.lang = lang
        if hasattr(self, "handlerCrudSingle"):
            self.handlerCrudSingle.set_language(lang)

    def return_mutation(self) -> ResponseGQL:
        return ResponseGQL(
            self.get_http_code(), [self.get_message()], [self.get_error()], [self.get_data()]
        )

    def set_crud(self, ddbb: Any, crudOptions: CrudOptions = None) -> None:
        self._set_internal_crud(ddbb, crudOptions)
        self._set_crud_for_validator()

    def _set_internal_crud(self, ddbb: Any, crudOptions: CrudOptions = None) -> None:
        self.handlerCrudSingle: CrudOne = CrudOne(ddbb, self.lang)
        self.handlerCrudSingle.set_collection(self.collection)
        self.handlerCrudSingle.set_language(self.lang)

        if crudOptions:
            self.set_crud_options(crudOptions)

    def _set_crud_for_validator(self) -> None:
        self.validator.crud = self.handlerCrudSingle

    def set_crud_options(self, options: CrudOptions) -> None:
        options.set_language(self.lang)
        self.handlerCrudSingle.set_options(options)

    def set_schema(self, entry: TData) -> None:
        self.schema = entry

    def set_schema_from_id(self, id: str) -> None:
        self.schema = {"_id": id}

    def get_message(self) -> str:
        return self.message

    def get_error(self) -> Union[str, Dict[str, str]]:
        return self.error

    def get_http_code(self) -> TData:
        return self.handlerCrudSingle.get_http_code()

    def get_data(self) -> TData:
        return self.data

    def reset_errors(self) -> None:
        self.error = {}

    async def get_all(self, **filter: Dict) -> List[TData]:
        return await self.handlerCrudSingle.get(**filter)

    async def get_single(self, **filter: Any) -> TData:
        return await self.handlerCrudSingle.get_single(**filter)

    async def get_by_id(self, id: Union[str, ObjectId], **filter: Any) -> TData:
        return await self.handlerCrudSingle.get_by_id(id, **filter)

    async def get_with_limit(self, limit: int = 1, sort: List[Tuple] = [], **filter: Any) -> TData:
        return await self.handlerCrudSingle.get_with_limit(limit, *sort, **filter)

    async def reference_resolver(self, info: Any) -> Optional[Dict]:
        data_id: Optional[str] = self._getIDFromEntry(raiseException=False)
        return (
            await AriadneDataLoader.for_context(info.context, self).load(data_id)
            if fn.isValidObjectId(data_id)
            else None
        )

    async def insert_update(self) -> None:
        await self.validate_to_insertUpdate()
        await self.insert_update_after_validation()

    async def insert_update_after_validation(self) -> None:
        await self.handlerCrudSingle.insert_update(self.schema)
        self._postprocess()

    def _postprocess(self) -> None:
        self.message = self.handlerCrudSingle.get_message()
        self.data = self.handlerCrudSingle.get_data()
        self.error = self.handlerCrudSingle.get_error()
        self.code = self.handlerCrudSingle.get_http_code()

    async def delete(self) -> None:
        await self.validate_to_delete()
        await self.delete_after_validation()

    async def delete_after_validation(self) -> None:
        _id = self._getIDFromEntry()
        await self.handlerCrudSingle.delete(_id)
        self._postprocess()

    def _is_empty(self) -> bool:
        if self._is_empty_data():
            raise err.ErrorEmptyData(self.error)
        return False

    def _is_empty_data(self) -> bool:
        if not bool(self.schema):
            self.error = self._set_error_when_empty_data()
            return True
        return False

    def _set_error_when_empty_data(self) -> str:
        return (
            self.translate("ERROR_EMPTY_FILE")
            if self._is_bulk_upload()
            else self.translate("ERROR_EMPTY_DATA")
        )

    def _getIDFromEntry(self, raiseException: bool = True) -> Union[str, None]:
        if bool(self.schema.get("id")):
            return str(self.schema.get("id"))
        elif bool(self.schema.get("_id")):
            return str(self.schema.get("_id"))

        if raiseException:
            self.error = self.translate("ERROR_MISSING_ID")
            raise err.ErrorInvalidID(self.error)

        return None

    def translate(self, msg: str) -> str:
        msg = tr.translate(msg, self.lang)
        schema: TData = copy.deepcopy(self.schema)
        if not bool(schema):
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
            if elm in schema:
                del schema[elm]
        return msg.format(schema)

    async def patch(self) -> None:
        if not await self._is_insert():
            self.schema = {**self.originalData, **self.schema}

    async def _is_insert(self) -> bool:
        if self._has_id():
            await self._retrieve_original_data_if_exists()
            return not self._is_already_inserted_in_ddbb()
        return True

    def _has_id(self) -> bool:
        return "id" in self.schema or "_id" in self.schema

    async def _retrieve_original_data_if_exists(self) -> None:
        id = self.schema["_id"] if self.schema.get("_id") else self.schema["id"]
        self.originalData = await self.get_by_id(str(id)) if id else {}

    def _is_already_inserted_in_ddbb(self) -> bool:
        return bool(self.originalData)
