from datetime import datetime
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
    DEACTIVATE_DATE,
    OMIT_FIELDS,
    CREATE,
    UPDATE,
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

# Kurt USERID
USER = "02477c69-56f4-4e77-921a-23a2a82a335e"
PROJECT_ID = "12070c789f30472094bbcf61923ecab4"


class collection:
    CRUD = "crud"
    CHANGELOG = "changeLog"


class TestCRUD_InsertOne:
    crud: CrudOne = CrudOne(mongo_db)
    crud.set_collection(collection.CRUD)

    async def test_insert_empty_data(self) -> None:
        entry: TData = {}
        with pytest.raises(ErrorCRUD) as excinfo:
            await self.crud.insert_update(entry)

        assertErrorInsertOne(self.crud, excinfo, HTTPCode.CODE_400)

    async def test_insert_invalid_id(self) -> None:
        entry: TData = {"id": 1}
        with pytest.raises(ErrorCRUD) as excinfo:
            await self.crud.insert_update(entry)

        assertErrorInsertOne(self.crud, excinfo, HTTPCode.CODE_400)

    async def test_insert_invalid_id_2(self) -> None:
        entry: TData = {"_id": 1}
        with pytest.raises(ErrorCRUD) as excinfo:
            await self.crud.insert_update(entry)

        assertErrorInsertOne(self.crud, excinfo, HTTPCode.CODE_400)

    async def test_insert_valid_data_without_id(self) -> None:
        entry: TData = {"one": 1}
        await self.crud.insert_update(entry)

        assertInsert(self.crud, entry, "MSG_SUCCESSFULLY_INSERTED")

    async def test_insert_valid_data_with_id_null(self) -> None:
        entry: TData = {"id": None, "one": 1}
        self.crud.lang = "es"
        self.crud.options.lang = "es"
        await self.crud.insert_update(entry)

        assertInsert(self.crud, entry, "MSG_SUCCESSFULLY_INSERTED")

    async def test_insert_valid_data_with_id_null_2(self) -> None:
        entry: TData = {"_id": None, "one": 1}
        await self.crud.insert_update(entry)

        assertInsert(self.crud, entry, "MSG_SUCCESSFULLY_INSERTED")

    async def test_insert_valid_data_with_id_empty_string(self) -> None:
        entry: TData = {"id": "", "one": 1}
        await self.crud.insert_update(entry)

        assertInsert(self.crud, entry, "MSG_SUCCESSFULLY_INSERTED")

    async def test_insert_valid_data_with_id_empty_string_2(self) -> None:
        entry: TData = {"_id": "", "one": 1}
        await self.crud.insert_update(entry)

        assertInsert(self.crud, entry, "MSG_SUCCESSFULLY_INSERTED")

    async def test_insert_valid_data_with_valid_id(self) -> None:
        entry: TData = {"id": ObjectId(), "one": 1}
        await self.crud.insert_update(entry)

        assertInsert(self.crud, entry, "MSG_SUCCESSFULLY_INSERTED")

    async def test_insert_valid_data_with_valid_id_2(self) -> None:
        entry: TData = {"_id": ObjectId(), "one": 1}
        await self.crud.insert_update(entry)

        assertInsert(self.crud, entry, "MSG_SUCCESSFULLY_INSERTED")

    async def test_schema_is_empty_after_insert(self) -> None:
        ID: str = str(ObjectId())
        entry: TData = {"id": ID, "one": 1}
        await self.crud.insert_update(entry)

        assert not bool(self.crud.schema)

    async def test_schema_is_empty_after_insert_with_error(self) -> None:
        entry: TData = {"id": "a", "one": 1}
        with pytest.raises(ErrorCRUD):
            await self.crud.insert_update(entry)

        assert not bool(self.crud.schema)

    async def test_check_history_after_insert(self) -> None:
        ID = ObjectId()
        entry: TData = {"_id": ID, "one": 1}
        await self.crud.insert_update(entry)

        self.crud.set_collection(collection.CHANGELOG)
        listChangelog: List[TData] = await self.crud.get(**{"parentID": str(ID)})

        assert len(listChangelog) == 1
        assert listChangelog[0]["action"] == CREATE
        assert listChangelog[0][collection.CHANGELOG] == []

    async def test_no_project_provided_in_crudOptions_empty(self) -> None:
        ID = ObjectId()
        entry: TData = {"_id": ID, "one": 1}
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        crud.set_options(CrudOptions(PROJECT_ID, USER))

        crud.lang = "en"
        crud.options.lang = "en"

        await crud.insert_update(entry)
        data: Dict = crud.data

        assert data.get("projectId") == PROJECT_ID

    async def test_no_project_provided_in_crudOptions_default(self) -> None:
        ID = ObjectId()
        entry: TData = {"_id": ID, "one": 1}

        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        crud.set_options(CrudOptions(projectId=""))

        await crud.insert_update(entry)
        data = crud.data

        assert data.get("projectId") is None

    async def test_project_provided_in_crudOptions(self) -> None:
        ID = ObjectId()
        entry: TData = {"_id": ID, "one": 1}

        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        crud.set_options(CrudOptions(projectId="TEST"))

        await crud.insert_update(entry)
        data = crud.data

        assert data["project"]["id"] == "TEST"


class TestCRUD_UpdateOne:
    crud: CrudOne = CrudOne(mongo_db)
    crud.set_collection(collection.CRUD)

    async def test_update_with_ObjectId(self) -> None:
        entry: TData = {"_id": ObjectId(), "one": 1}
        await self.crud.insert_update(entry)

        entry["one"] = 2
        await self.crud.insert_update(entry)

        assertUpdate(self.crud, entry, "MSG_SUCCESSFULLY_UPDATED")

    async def test_update_with_ObjectId_2(self) -> None:
        entry: TData = {"id": ObjectId(), "one": 1}
        await self.crud.insert_update(entry)

        entry["one"] = 2
        await self.crud.insert_update(entry)

        assertUpdate(self.crud, entry, "MSG_SUCCESSFULLY_UPDATED")

    async def test_update_without_ObjectId(self) -> None:
        ID: str = str(ObjectId())
        entry: TData = {"id": ID, "one": 1}
        await self.crud.insert_update(entry)

        entry["one"] = 2
        await self.crud.insert_update(entry)

        assertUpdate(self.crud, entry, "MSG_SUCCESSFULLY_UPDATED")

    async def test_update_without_ObjectId_2(self) -> None:
        ID: str = str(ObjectId())
        entry: TData = {"id": ID, "one": 1}
        await self.crud.insert_update(entry)

        entry["one"] = 2
        await self.crud.insert_update(entry)

        assertUpdate(self.crud, entry, "MSG_SUCCESSFULLY_UPDATED")

    async def test_update_with_ObjectId_active_false(self) -> None:
        entry: TData = {"_id": ObjectId(), "active": True}
        await self.crud.insert_update(entry)

        entry["active"] = False
        await self.crud.insert_update(entry)

        assert DEACTIVATE_DATE in self.crud.get_data()
        assert self.crud.get_data().get(DEACTIVATE_DATE)
        assertUpdate(self.crud, entry, "MSG_SUCCESSFULLY_UPDATED")

    async def test_update_with_ObjectId_active_true(self) -> None:
        entry: TData = {"_id": ObjectId(), "active": False, "deactivateDate": datetime.utcnow()}
        await self.crud.insert_update(entry)

        entry["active"] = True
        await self.crud.insert_update(entry)

        assert self.crud.get_data().get(DEACTIVATE_DATE, False) is None

        assertUpdate(self.crud, entry, "MSG_SUCCESSFULLY_UPDATED")

    async def test_update_with_ObjectId_active_true_false_true(self) -> None:
        entry: TData = {"_id": ObjectId(), "active": False, "deactivateDate": datetime.utcnow()}
        await self.crud.insert_update(entry)

        entry["active"] = True
        await self.crud.insert_update(entry)

        entry["active"] = False
        await self.crud.insert_update(entry)

        assert DEACTIVATE_DATE in self.crud.get_data()
        assert self.crud.get_data().get(DEACTIVATE_DATE)

        assertUpdate(self.crud, entry, "MSG_SUCCESSFULLY_UPDATED")

    async def test_insert_active_false_deactivateDate(self) -> None:
        entry: TData = {"_id": ObjectId(), "active": False}
        await self.crud.insert_update(entry)

        assert DEACTIVATE_DATE in self.crud.get_data()
        assert self.crud.get_data().get(DEACTIVATE_DATE)

        assertInsert(self.crud, entry, "MSG_SUCCESSFULLY_INSERTED")

    async def test_schema_is_empty_after_update(self) -> None:
        ID: str = str(ObjectId())
        await update_entry(ID, self.crud)

    async def test_check_history_after_update(self) -> None:
        ID: str = str(ObjectId())
        await update_entry(ID, self.crud)

        self.crud.set_collection(collection.CHANGELOG)
        listChangelog: List[TData] = await self.crud.get(**{"parentID": ID})

        assertChangeLogAfterUpdate(listChangelog)

    async def test_update_no_history_when_there_are_no_changes(self) -> None:
        entry: TData = {"_id": ObjectId(), "one": 1}
        await self.crud.insert_update(entry)
        await self.crud.insert_update(entry)
        modifiedData: TData = self.crud.get_data()
        msg: str = self.crud.get_message()

        assert MODIFIED_USER not in modifiedData
        assert MODIFIED_DATE not in modifiedData

        assert tr.translate("MESSAGE_NO_CHANGES_TO_UPDATE")[:-2] in msg

    async def test_update_no_history_created_when_there_are_no_changes(self) -> None:
        ID = ObjectId()
        entry: TData = {"_id": ID, "one": 1}
        await self.crud.insert_update(entry)
        await self.crud.insert_update(entry)

        self.crud.set_collection(collection.CHANGELOG)
        _filter: Dict = {"parentID": str(ID)}
        listChangelog: List[TData] = await self.crud.get(**_filter)

        assert len(listChangelog) == 1


async def update_entry(id: ObjectId, crud: CrudOne) -> None:
    entry: TData = {"id": id, "one": 1}
    await crud.insert_update(entry)
    assert not bool(crud.schema)

    entry["one"] = 2
    await crud.insert_update(entry)
    assert not bool(crud.schema)


def assertChangeLogAfterUpdate(listChangelog: List[TData]) -> None:
    assert len(listChangelog) == 2
    for changelog in listChangelog:
        if changelog["action"] == CREATE:
            assertChangeLogCreate(changelog)
        else:
            assertChangeLogUpdate(changelog, "one", "1", "2")


def assertChangeLogUpdate(changelog: TData, field: str, oldValue: str, newValue: str) -> None:
    assert changelog["action"] == UPDATE
    assert changelog[collection.CHANGELOG] == [
        {"field": field, "oldValue": oldValue, "newValue": newValue}
    ]


def assertChangeLogCreate(changelog: TData) -> None:
    assert changelog["action"] == CREATE
    assert changelog[collection.CHANGELOG] == []


def assert_createdData_equals_retievedData(createdData: TData, retrievedData: TData) -> None:
    for elm in createdData:
        if elm not in OMIT_FIELDS:
            assert createdData[elm] == retrievedData[elm]


async def insert_one_by_id(id: str, crud: CrudOne, **additionalData: Dict) -> TData:
    entry: TData = {"_id": ObjectId(id), "one": 1, **additionalData}
    await crud.insert_update(entry)
    return crud.get_data()[0]


def assertCreateCrudOptions(optCrud: CrudOptions) -> None:
    assert optCrud.projectId == PROJECT_ID
    assert optCrud.userId == USER
    assert optCrud.actionChangeLog == "Update"
    assert optCrud.omitFields == OMIT_FIELDS
    assert optCrud.updateAuditFields is True
    assert optCrud.updateChangeLog is True
    assert optCrud.softDelete is True
    assert optCrud.filterByUser is False


def assertErrorInsertOne(
    crud: CrudOne, excinfo: Any, http_code: HTTPCode = HTTPCode.CODE_400
) -> None:
    assert not bool(crud.get_message())
    assert bool(crud.get_error())
    assert not bool(crud.get_data())
    assert crud.http_code == http_code
    assert crud.get_error() == str(excinfo.value)


def assertErrorDelete(crud: CrudOne, excinfo: Any) -> None:
    assert bool(crud.get_message())
    assert not bool(crud.get_data())
    assert crud.get_message() == str(excinfo.value)


def assertCreateCRUDObject(crud: CrudOne) -> None:
    assert isinstance(crud.mongoDB, Database)
    assert isinstance(crud.messages, List)
    assert isinstance(crud.data, List)


def assertInsert(crud: CrudOne, entry: TData, msg: str) -> None:
    assert bool(crud.get_message())
    assert not bool(crud.get_error())
    assert bool(crud.get_data())
    assert crud.http_code == HTTPCode.CODE_200
    assertData(crud.get_data(), entry)
    assertMessage(crud.get_message(), msg, crud.lang)
    assert CREATE_DATE in crud.get_data()
    assert CREATE_USER in crud.get_data()
    assert MODIFIED_USER not in crud.get_data()
    assert MODIFIED_DATE not in crud.get_data()
    assert DELETED_USER not in crud.get_data()
    assert DELETED_DATE not in crud.get_data()


def assertUpdate(crud: CrudOne, entry: TData, msg: str) -> None:
    assert bool(crud.get_message())
    assert bool(crud.get_data())
    assert not bool(crud.get_error())
    assert crud.http_code == HTTPCode.CODE_200
    assertData(crud.get_data(), entry)
    assertMessage(crud.get_message(), msg, crud.lang)
    assert CREATE_DATE in crud.get_data()
    assert CREATE_USER in crud.get_data()
    assert MODIFIED_USER in crud.get_data()
    assert MODIFIED_DATE in crud.get_data()


def assertData(schema: TData, entry: TData) -> None:
    for elm in entry.keys():
        if elm in OMIT_FIELDS:
            continue
        assert schema[elm] == schema[elm]


def assertMessage(savedMessage: List[str], msg: str, lang: str = "en") -> None:
    assert tr.translate(msg, lang)[:30] in savedMessage
