import os
import sys
from typing import Any, Dict, List

import pytest

if os.getenv("MOCK_TEST") == "True":
    from mongomock import Database
else:
    from pymongo.database import Database

from bson import ObjectId

from conftest import mongo_db

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.http_codes import HTTPCode
from _python_core.crud.crud_constants import (
    OMIT_FIELDS,
    CREATE_DATE,
    CREATE_USER,
    DELETED_DATE,
    DELETED_USER,
    MODIFIED_DATE,
    MODIFIED_USER,
)
from _python_core.crud.crud import ErrorCRUD
from _python_core.crud.crud_single import CrudOne
from _python_core.crud.crud_options import CrudOptions
from _python_core.translations import Translations as tr

TData = Dict[str, Any]  # Type object as defined in GQL Schema

CREATE = "Create"
UPDATE = "Update"
DELETE = "Delete"

# Kurt USERID
USER = "02477c69-56f4-4e77-921a-23a2a82a335e"
PROJECT_ID = "12070c789f30472094bbcf61923ecab4"


class collection:
    CRUD = "crud"
    CHANGELOG = "changeLog"


class TestCRUD_Soft_Delete_One:
    crud: CrudOne = CrudOne(mongo_db)
    crud.set_collection(collection.CRUD)
    crud.options.set_softDelete(True)

    async def test_soft_delete(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        assertSoftDelete(self.crud, entry, "MSG_SUCCESSFULLY_SOFT_DELETED")

    async def test_soft_delete_error_unexisting_data(self) -> None:
        _id: str = str(ObjectId())
        with pytest.raises(ErrorCRUD) as excinfo:
            await self.crud.delete(_id)

        assertErrorDelete(self.crud, excinfo, HTTPCode.CODE_400)

    async def test_soft_delete_no_id(self) -> None:
        _id: str = ""
        with pytest.raises(ErrorCRUD) as excinfo:
            await self.crud.delete(_id)

        assertErrorDelete(self.crud, excinfo, HTTPCode.CODE_400)

    async def test_soft_delete_check_schema_empty_after_delete(self) -> None:
        await self.test_soft_delete()

        assert self.crud.schema == {}

    async def test_soft_delete_check_auditFields(self) -> None:
        await self.test_soft_delete()
        assert_delete_after_insert(self.crud)

    async def test_soft_delete_after_update(self) -> None:
        self.crud.collection = collection.CRUD
        await update_entry(self.crud)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        assert_soft_delete_after_update(self.crud)

    async def test_history_after_soft_delete(self) -> None:
        ID = ObjectId()
        entry: TData = {"_id": ID, "one": 1}
        await self.crud.insert_update(entry)
        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        deletedData: List[TData] = await self.crud.get(**{"parentID": delete_id})

        assertChangelog_soft_delete_after_insert(deletedData)
        assert_delete_after_insert(self.crud)

    async def test_data_exists_after_soft_delete(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        softDeletedData: TData = await self.crud.get_by_id(delete_id)
        assert bool(softDeletedData)

    async def test_data_get_by_id_after_soft_delete_dont_skip_deleted(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        self.crud.options.set_skipDeletedEntries(False)
        softDeletedData: TData = await self.crud.get_by_id(delete_id)
        assert delete_id == str(softDeletedData["_id"])
        self.crud.options.set_skipDeletedEntries(True)

    async def test_data_get_single_after_soft_delete_skip_deleted(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        _filter: Dict = {"_id": ObjectId(delete_id)}
        softDeletedData: TData = await self.crud.get_single(**_filter)
        assert not bool(softDeletedData)

    async def test_data_get_single_after_soft_delete_dont_skip_deleted(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        _filter: Dict = {"_id": ObjectId(delete_id)}
        self.crud.options.set_skipDeletedEntries(False)
        softDeletedData: TData = await self.crud.get_single(**_filter)
        assert delete_id == str(softDeletedData["_id"])
        self.crud.options.set_skipDeletedEntries(True)

    async def test_data_get_after_soft_delete_skip_deleted(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        _filter: Dict = {"_id": ObjectId(delete_id)}
        softDeletedData: List[TData] = await self.crud.get(**_filter)
        assert not bool(softDeletedData)

    async def test_data_get_after_soft_delete_dont_skip_deleted(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        _filter: Dict = {"_id": ObjectId(delete_id)}
        self.crud.options.set_skipDeletedEntries(False)
        softDeletedData: List[TData] = await self.crud.get(**_filter)
        assert delete_id == str(softDeletedData[0]["_id"])
        self.crud.options.set_skipDeletedEntries(True)

    async def test_data_get_with_limit_after_soft_delete_skip_deleted(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        _filter: Dict = {"_id": ObjectId(delete_id)}
        softDeletedData: List[TData] = await self.crud.get_with_limit(limit=1, **_filter)
        assert not bool(softDeletedData)

    async def test_data_get_with_limit_after_soft_delete_dont_skip_deleted(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        _filter: Dict = {"_id": ObjectId(delete_id)}
        self.crud.options.set_skipDeletedEntries(False)
        softDeletedData: List[TData] = await self.crud.get_with_limit(limit=1, **_filter)
        assert delete_id == str(softDeletedData[0]["_id"])
        self.crud.options.set_skipDeletedEntries(True)


class TestCRUD_Hard_Delete_One:
    crud: CrudOne = CrudOne(mongo_db)
    crud.set_collection(collection.CRUD)
    crud.options.set_softDelete(False)

    async def test_hard_delete(self) -> None:
        self.crud.options.softDelete = False
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        assert tr.translate("MSG_SUCCESSFULLY_HARD_DELETED")[:-2] in self.crud.get_message()

    async def test_hard_delete_error_unexisting_data(self) -> None:
        self.crud.options.softDelete = True
        _id: str = str(ObjectId())
        with pytest.raises(ErrorCRUD) as excinfo:
            await self.crud.delete(_id)

        assertErrorDelete(self.crud, excinfo, HTTPCode.CODE_400)

    async def test_hard_delete_check_schema_empty_after_delete(self) -> None:
        await self.test_hard_delete()

        assert self.crud.schema == {}

    async def test_hard_delete_check_auditFields(self) -> None:
        await self.test_hard_delete()
        assert_hard_delete_after_insert(self.crud)

    async def test_hard_delete_after_update(self) -> None:
        self.crud.collection = collection.CRUD
        await update_entry(self.crud)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        assert_hard_delete_after_update(self.crud)

    async def test_data_get_after_hard_delete_skip_deleted(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        _filter: Dict = {"_id": ObjectId(delete_id)}
        softDeletedData: List[TData] = await self.crud.get(**_filter)
        assert not bool(softDeletedData)

    async def test_data_get_after_hard_delete_dont_skip_deleted(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        delete_id: str = str(self.crud.data["_id"])
        await self.crud.delete(delete_id)

        _filter: Dict = {"_id": ObjectId(delete_id)}
        softDeletedData: List[TData] = await self.crud.get(skip_soft_deleted=False, **_filter)
        assert not bool(softDeletedData)


def assertChangelog_soft_delete_after_insert(listChangelog: List[TData]) -> None:
    for changelog in listChangelog:
        if changelog["action"] in [CREATE, DELETE]:
            assert changelog[collection.CHANGELOG] == []


async def update_entry(crud: CrudOne) -> None:
    entry: TData = {"one": 1}
    await crud.insert_update(entry)
    entry = crud.get_data()
    entry["one"] = 2
    await crud.insert_update(entry)


def assert_hard_delete_after_insert(crud: CrudOne) -> None:
    data: TData = crud.get_data()
    assert_hard_delete_after_insert_only_data(data)


def assert_hard_delete_after_insert_only_data(data: TData) -> None:
    assert CREATE_DATE in data
    assert CREATE_USER in data
    assert MODIFIED_DATE not in data
    assert MODIFIED_USER not in data
    assert DELETED_DATE not in data
    assert DELETED_USER not in data


def assert_delete_after_insert(crud: CrudOne) -> None:
    data: TData = crud.get_data()
    assert_soft_delete_after_insert_only_data(data)


def assert_soft_delete_after_insert_only_data(data: TData) -> None:
    assert CREATE_DATE in data
    assert CREATE_USER in data
    assert MODIFIED_DATE not in data
    assert MODIFIED_USER not in data
    assert DELETED_DATE in data
    assert DELETED_USER in data


def assert_hard_delete_after_update(crud: CrudOne) -> None:
    data: TData = crud.get_data()
    assert_hard_delete_after_update_only_data(data)


def assert_hard_delete_after_update_only_data(data: TData) -> None:
    assert CREATE_DATE in data
    assert CREATE_USER in data
    assert MODIFIED_DATE in data
    assert MODIFIED_USER in data
    assert DELETED_DATE not in data
    assert DELETED_USER not in data


def assert_soft_delete_after_update(crud: CrudOne) -> None:
    data: TData = crud.get_data()
    assert_soft_delete_after_update_only_data(data)


def assert_soft_delete_after_update_only_data(data: TData) -> None:
    assert CREATE_DATE in data
    assert CREATE_USER in data
    assert MODIFIED_DATE in data
    assert MODIFIED_USER in data
    assert DELETED_DATE in data
    assert DELETED_USER in data


def assert_createdData_equals_retievedData(createdData: TData, retrievedData: TData) -> None:
    for elm in createdData:
        if elm not in OMIT_FIELDS:
            assert createdData[elm] == retrievedData[elm]


async def insert_one_by_id(_id: str, crud: CrudOne, **additionalData: Dict) -> TData:
    entry: TData = {"_id": ObjectId(id), "one": 1, **additionalData}
    await crud.insert_update(entry)
    return crud.get_data()


def assertCreateCrudOptions(optCrud: CrudOptions) -> None:
    assert optCrud.projectId == PROJECT_ID
    assert optCrud.userId == USER
    assert optCrud.actionChangeLog == "Update"
    assert optCrud.omitFields == OMIT_FIELDS
    assert optCrud.updateAuditFields is True
    assert optCrud.updateChangeLog is True
    assert optCrud.softDelete is True
    assert optCrud.filterByUser is False


def assertErrorInsertOne(crud: CrudOne, excinfo: Any) -> None:
    assert not bool(crud.get_message())
    assert not bool(crud.get_data())
    assert bool(crud.get_error())
    assert crud.get_error() == str(excinfo.value)


def assertErrorDelete(
    crud: CrudOne, excinfo: Any, http_code: HTTPCode = HTTPCode.CODE_400
) -> None:
    assert not bool(crud.get_message())
    assert not bool(crud.get_data())
    assert bool(crud.get_error())
    assert crud.get_error() == str(excinfo.value)
    assert crud.http_code == http_code


def assertCreateCRUDObject(crud: CrudOne) -> None:
    assert isinstance(crud.mongoDB, Database)
    assert isinstance(crud.message, List)
    assert isinstance(crud.data, List)


def assertInsert(crud: CrudOne, entry: TData, msg: str) -> None:
    assert bool(crud.get_message())
    assert bool(crud.get_data())
    assertData(crud.get_data(), entry)
    assertMessage(crud.get_message(), msg, crud.lang)
    assert CREATE_DATE in crud.get_data()
    assert CREATE_USER in crud.get_data()
    assert MODIFIED_USER not in crud.get_data()
    assert MODIFIED_DATE not in crud.get_data()


def assertUpdate(crud: CrudOne, entry: TData, msg: str) -> None:
    assert bool(crud.get_message())
    assert bool(crud.get_data())
    assertData(crud.get_data(), entry)
    assertMessage(crud.get_message(), msg, crud.lang)
    assert CREATE_DATE in crud.get_data()
    assert CREATE_USER in crud.get_data()
    assert MODIFIED_USER in crud.get_data()
    assert MODIFIED_DATE in crud.get_data()


def assertSoftDelete(crud: CrudOne, entry: TData, msg: str) -> None:
    assert bool(crud.get_message())
    assert bool(crud.get_data())
    assert crud.http_code == HTTPCode.CODE_200
    assertData(crud.get_data(), entry)
    assertMessage(crud.get_message(), msg, crud.lang)
    assert CREATE_DATE in crud.get_data()
    assert CREATE_USER in crud.get_data()
    assert DELETED_DATE in crud.get_data()
    assert DELETED_USER in crud.get_data()


def assertData(schema: TData, entry: TData) -> None:
    for elm in entry.keys():
        if elm in OMIT_FIELDS:
            continue
        assert schema[elm] == entry[elm]


def assertMessage(returnedMessage: str, msg: str, lang: str = "en") -> None:
    assert tr.translate(msg, lang)[:30] in returnedMessage
