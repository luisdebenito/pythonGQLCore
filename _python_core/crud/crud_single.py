import copy
from datetime import datetime
from typing import Any, Dict, List, TypeVar, Union

from bson import ObjectId
from pymongo import MongoClient, ReturnDocument
from pymongo.results import InsertOneResult

from _python_core.crud.crud import Crud, ErrorCRUD
from _python_core.crud.crud_constants import (
    ACTIVE,
    CREATE,
    CREATE_DATE,
    CREATE_USER,
    DEACTIVATE_DATE,
    DELETE,
    DELETED_DATE,
    DELETED_USER,
    MODIFIED_DATE,
    MODIFIED_USER,
    UPDATE,
)
from _python_core.crud.crud_options import CrudOptions
from _python_core.history import History
from _python_core.http_codes import HTTPCode
from _python_core.translations import Translations as tr

TData = Dict[str, Any]  # Type object as defined in GQL Schema
TMessages = List[str]
TInsertedData = List[TData]

TCrud = TypeVar("TCrud", bound="Crud")
TCrudOne = TypeVar("TCrudOne", bound="CrudOne")


class CrudOne(Crud):
    def __init__(self, mongo: MongoClient, lang: str = "en") -> None:
        super().__init__(mongo, lang)
        self._initialize_values()

    def _initialize_values(self) -> None:
        self.schema: TData = {}
        self.message: str = ""
        self.error: str = ""
        self.data: TData = {}
        self.originalData: TData = {}

    @classmethod
    def copy(cls, crudOne: TCrudOne) -> TCrudOne:
        newCrud = cls(crudOne.mongoDB)
        newCrud.set_collection(crudOne.collection)
        return newCrud

    def set_language(self, lang: str) -> None:
        self.lang = lang
        self.options.lang = lang

    def set_options(self, options: CrudOptions) -> None:
        self.options = options
        self._verifyLanguage()

    def set_collection(self, collection: str) -> None:
        self.collection = collection
        self.mongo = self.mongoDB[self.collection]

    def request_postprocess(func: Any) -> Any:
        async def wrapped(crud: Crud, data: Union[str, Dict], *args, **kwargs: Dict) -> Dict:  # type: ignore
            try:
                await func(crud, data, *args, **kwargs)
                crud.http_code = HTTPCode.CODE_200  # type: ignore
            except (ErrorCRUD, AssertionError) as err:
                raise ErrorCRUD(str(err)) from err
            finally:
                crud.postprocess()

        return wrapped

    def postprocess(self) -> None:
        self.schema = {}
        self.http_code = self.http_code if bool(self.http_code) else HTTPCode.CODE_500  # type: ignore

    @request_postprocess
    async def insert_update(self, schema: TData) -> None:
        self.schema = schema
        self._reset_message_errors_and_data()
        self._check_valid_schema()
        self._tweak_entry()

        await self._insert() if await self._is_insert() else await self._update()

    def _tweak_entry(self) -> None:
        self._tweak_null_or_empty_id()
        self._tweak_non_null_non_empty_id()
        self._tweak_add_project_if_needed()

    def _tweak_add_project_if_needed(self) -> None:
        if self.options.projectId and self.schema:
            self.schema["projectId"] = self.options.projectId
            self.schema["project"] = {"id": self.options.projectId}

    def _tweak_null_or_empty_id(self) -> None:
        if "id" in self.schema and not bool(self.schema["id"]):
            del self.schema["id"]
        elif "_id" in self.schema and not bool(self.schema["_id"]):
            del self.schema["_id"]

    def _tweak_non_null_non_empty_id(self) -> None:
        self._tweak_entry_with_id()
        self._tweak_entry_with_underscore_id()

    def _tweak_entry_with_id(self) -> None:
        if "id" in self.schema:
            if self._is_id_valid():
                self.schema["_id"] = ObjectId(str(self.schema["id"]))
                del self.schema["id"]
            else:
                self._raise_error("ERROR_INVALID_ID")

    def _tweak_entry_with_underscore_id(self) -> None:
        if "_id" in self.schema:
            if self._is_id_valid():
                self.schema["_id"] = ObjectId(str(self.schema["_id"]))
            else:
                self._raise_error("ERROR_INVALID_ID")

    def _check_valid_schema(self) -> bool:
        return all([not self._is_empty_data()])

    def _is_empty_data(self) -> bool:
        if not bool(self.schema):
            self._raise_error("ERROR_EMPTY_SCHEMA")
        return False

    def _raise_error(self, msg: str, http_code: HTTPCode = HTTPCode.CODE_400) -> None:
        self.error = self.translate(msg)
        self.http_code = http_code
        raise ErrorCRUD(self.error)

    async def _is_insert(self) -> bool:
        await self._retrieve_original_data_if_exists()
        return not self._is_already_inserted_in_ddbb() if self._has_id() else True

    def _has_id(self) -> bool:
        return "id" in self.schema or "_id" in self.schema

    def _is_id_valid(self) -> bool:
        if "id" in self.schema:
            return self._is_id_a_valid_objectId(str(self.schema["id"]))
        elif "_id" in self.schema:
            return self._is_id_a_valid_objectId(str(self.schema["_id"]))

        return False

    async def _retrieve_original_data_if_exists(self) -> None:
        self.originalData = (
            await self.get_by_id(str(self.schema["_id"])) if self.schema.get("_id") else {}
        )

    def _is_already_inserted_in_ddbb(self) -> bool:
        return bool(self.originalData)

    async def _insert(self) -> None:
        result = self._insert_in_database()
        await self._process_after_insert(result)

    def _insert_in_database(self) -> InsertOneResult:
        self._add_audit_fields_to_insert()
        return self.mongo.insert_one(self.schema)

    async def _process_after_insert(self, result: InsertOneResult) -> None:
        if result.inserted_id:
            await self._process_after_insert_OK(result)
        else:
            self._raise_error("ERROR_UNKNOWN_MONGO_INSERT", HTTPCode.CODE_500)

    async def _process_after_insert_OK(self, result: InsertOneResult) -> None:
        self.schema = await self.get_by_id(result.inserted_id)
        self.data = copy.deepcopy(self.schema)
        self.message = self.translate("MSG_SUCCESSFULLY_INSERTED")
        if self._is_update_changelog():
            await self._save_changelog(self.schema, CREATE)

    def _add_audit_fields_to_insert(self) -> None:
        if self.options.updateAuditFields:
            self.schema[CREATE_USER] = {"id": self.options.userId}
            self.schema[CREATE_DATE] = datetime.utcnow()
            self._set_deactivate_audit_fields()

    def _is_update_changelog(self) -> bool:
        return self.options.updateChangeLog

    async def _save_changelog(self, entry: TData, action: str = UPDATE) -> None:
        historyClass: History = self._config_changelog(entry, action)
        await historyClass.calculate(self.mongoDB)
        history: TData = historyClass.get()

        await self._save_changelog_in_database(history)

    def _config_changelog(self, entry: TData, action: str = UPDATE) -> History:
        history: History = History(entry)
        history.set_collection(self.collection)
        history.set_action(action)
        return history

    async def _save_changelog_in_database(self, history: TData) -> None:
        changelog_crud_options: CrudOptions = self._set_changelog_crud_options()
        changelog_crud: CrudOne = self._set_changelog_crud(changelog_crud_options)
        await changelog_crud.insert_update(history)

    def _set_changelog_crud(self, changelog_crud_options: CrudOptions) -> TCrudOne:
        changelog_crud: CrudOne = CrudOne(self.mongoDB, lang=changelog_crud_options.lang)
        changelog_crud.set_collection(History.collection)
        changelog_crud.set_options(changelog_crud_options)
        return changelog_crud

    def _set_changelog_crud_options(self) -> CrudOptions:
        changelog_crud_options: CrudOptions = copy.deepcopy(self.options)
        changelog_crud_options.set_updateAuditFields(True)
        changelog_crud_options.set_updateChangeLog(False)
        return changelog_crud_options

    async def _update(self) -> None:
        self._patch()
        if await self._there_are_changes():
            await self._update_if_there_are_changes_in_schema()
        else:
            self.data = copy.deepcopy(self.schema)
            self.message = self.translate("MESSAGE_NO_CHANGES_TO_UPDATE")

    def _patch(self) -> None:
        self.schema = {**self.originalData, **self.schema}

    async def _update_if_there_are_changes_in_schema(self) -> None:
        await self._process_before_update()
        data: TData = self._update_in_database()
        await self._process_after_update(data)

    async def _process_before_update(self) -> None:
        if self._is_update_changelog():
            await self._save_changelog(self.schema, UPDATE)

    def _update_in_database(self) -> TData:
        self._add_audit_fields_to_update()
        return self.mongo.find_one_and_update(
            {"_id": ObjectId(self.schema["_id"])},
            {"$set": self.schema},
            return_document=ReturnDocument.AFTER,
        )

    async def _process_after_update(self, data: TData) -> None:
        if data:
            self.data = data
            self.message = self.translate("MSG_SUCCESSFULLY_UPDATED")
        else:
            self._raise_error("ERROR_UNKNOWN_MONGO_UPDATE", HTTPCode.CODE_500)

    async def _there_are_changes(self) -> bool:
        historyClass: History = self._config_changelog(self.schema, UPDATE)
        await historyClass.calculate(self.mongoDB)
        history: TData = historyClass.get()
        return len(history[History.collection]) > 0

    def _add_audit_fields_to_update(self) -> None:
        if self.options.updateAuditFields:
            self._set_modified_audit_fields()
            self._set_deactivate_audit_fields()

    def _set_modified_audit_fields(self) -> None:
        self.schema[MODIFIED_USER] = {"id": self.options.userId}
        self.schema[MODIFIED_DATE] = datetime.utcnow()

    def _set_deactivate_audit_fields(self) -> None:
        if self.schema.get(ACTIVE) is False and not self.schema.get(DEACTIVATE_DATE):
            self.schema[DEACTIVATE_DATE] = datetime.utcnow()
        elif self.schema.get(ACTIVE) is True and self.schema.get(DEACTIVATE_DATE):
            self.schema[DEACTIVATE_DATE] = None

    @request_postprocess
    async def delete(self, id: str) -> None:
        self.schema = {"_id": id}
        self._reset_message_errors_and_data()
        self._check_valid_id_for_delete()
        await self._check_existing_data(id)

        await self._soft_delete() if self._is_soft_delete() else await self._hard_delete()

    def _check_valid_id_for_delete(self) -> None:
        if not self._is_id_valid():
            self._raise_error("ERROR_INVALID_ID", HTTPCode.CODE_400)

    async def _soft_delete(self) -> None:
        data = self._soft_delete_in_database()
        await self._process_after_delete(data)

    def _soft_delete_in_database(self) -> TData:
        self._add_audit_fields_to_delete()
        return self.mongo.find_one_and_update(
            {"_id": ObjectId(self.schema["_id"])},
            {"$set": self.schema},
            return_document=ReturnDocument.AFTER,
        )

    async def _process_after_delete(self, data: TData) -> None:
        if data:
            await self._process_after_delete_OK(data)
        else:
            self._process_after_delete_Error()

    def _process_after_delete_Error(self) -> None:
        msg_error: str = (
            "ERROR_UNKNOWN_MONGO_SOFT_DELETE"
            if self._is_soft_delete()
            else "ERROR_UNKNOWN_MONGO_HARD_DELETE"
        )
        self._raise_error(msg_error, HTTPCode.CODE_500)

    async def _process_after_delete_OK(self, data: TData) -> None:
        self.data = data
        msg_changelog: str = (
            "MSG_SUCCESSFULLY_SOFT_DELETED"
            if self._is_soft_delete()
            else "MSG_SUCCESSFULLY_HARD_DELETED"
        )
        self.message = self.translate(msg_changelog)
        if self._is_update_changelog():
            await self._save_changelog(data, DELETE)

    def _add_audit_fields_to_delete(self) -> None:
        if self.options.updateAuditFields:
            self.schema[DELETED_USER] = {"id": self.options.userId}
            self.schema[DELETED_DATE] = datetime.utcnow()

    async def _hard_delete(self) -> None:
        data = self._hard_delete_in_database()
        await self._process_after_delete(data)

    def _hard_delete_in_database(self) -> TData:
        return self.mongo.find_one_and_delete({"_id": ObjectId(self.schema["_id"])})

    def _is_soft_delete(self) -> bool:
        return self.options.softDelete

    async def _check_existing_data(self, id: str) -> None:
        self.schema = await self.get_by_id(id)
        if not bool(self.schema):
            self._raise_error("ERROR_UNEXISTING_DATA")

    def translate(self, msg: str) -> str:
        return self._translate_with_schema(msg) if self.schema else tr.translate(msg, self.lang)

    def _translate_with_schema(self, msg: str) -> str:
        entry = copy.deepcopy(self.schema)
        for elm in self.options.omitFields:
            if elm in entry:
                del entry[elm]
        return tr.translate(msg, self.lang).format(entry)

    def _reset_message_errors_and_data(self) -> None:
        self._reset_error()
        self._reset_message()
        self._reset_data()

    def _reset_message(self) -> None:
        self.message = ""

    def _reset_data(self) -> None:
        self.data = {}

    def _reset_error(self) -> None:
        self.error = ""

    def get_message(self) -> str:
        return self.message

    def get_data(self) -> TData:
        return self.data

    def get_error(self) -> str:
        return self.error

    def get_http_code(self) -> HTTPCode:
        return self.http_code
