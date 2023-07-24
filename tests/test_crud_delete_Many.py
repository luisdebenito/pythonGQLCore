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
from _python_core.crud.crud_many import CrudMany
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


class TestCRUD_Soft_Delete_Many:
    crudMany: CrudMany = CrudMany(mongo_db)
    crudMany.set_collection(collection.CRUD)
    crudMany.options.set_softDelete(True)

    async def test_soft_delete_one(self) -> None:
        ID1: ObjectId = ObjectId()
        entries: List[TData] = [{"_id": ID1, "one": 1}]
        await self.crudMany.insert_update(entries)
        await self.crudMany.delete([str(ID1)])

        assertSoftDeleteMany(
            self.crudMany,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200],
            ["MSG_SUCCESSFULLY_SOFT_DELETED"],
            [[CREATE, DELETE]],
        )

    async def test_soft_delete_many(self) -> None:
        ID1: ObjectId = ObjectId()
        ID2: ObjectId = ObjectId()
        entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
        await self.crudMany.insert_update(entries)
        await self.crudMany.delete([str(ID1), str(ID2)])

        assertSoftDeleteMany(
            self.crudMany,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200, HTTPCode.CODE_200],
            ["MSG_SUCCESSFULLY_SOFT_DELETED", "MSG_SUCCESSFULLY_SOFT_DELETED"],
            [[CREATE, DELETE], [CREATE, DELETE]],
        )

    async def test_soft_delete_error_no_data_provided(self) -> None:
        entries: List[str] = []
        await self.crudMany.delete(entries)

        assert len(self.crudMany.get_errors()) == 1
        assert self.crudMany.get_errors()[0] == tr.translate("ERROR_EMPTY_SCHEMA")

    async def test_soft_delete_one_ok_other_unexisting(self) -> None:
        ID1: ObjectId = ObjectId()
        entries: List[TData] = [{"_id": ID1, "one": 1}]
        await self.crudMany.insert_update(entries)
        await self.crudMany.delete([str(ID1), str(ObjectId())])

        assertSoftDeleteMany(
            self.crudMany,
            HTTPCode.CODE_400,
            [HTTPCode.CODE_200, HTTPCode.CODE_400],
            ["MSG_SUCCESSFULLY_SOFT_DELETED"],
            [[CREATE, DELETE]],
        )
        assert len(self.crudMany.get_errors()) == 1
        assert self.crudMany.get_errors()[0] == tr.translate("ERROR_UNEXISTING_DATA")

    async def test_soft_delete_error_unexisting_data(self) -> None:
        await self.crudMany.delete([str(ObjectId()), str(ObjectId())])

        assertSoftDeleteMany(
            self.crudMany,
            HTTPCode.CODE_400,
            [HTTPCode.CODE_400, HTTPCode.CODE_400],
            [],
            [],
        )
        assert len(self.crudMany.get_errors()) == 2
        assert self.crudMany.get_errors()[0] == tr.translate("ERROR_UNEXISTING_DATA")
        assert self.crudMany.get_errors()[1] == tr.translate("ERROR_UNEXISTING_DATA")

    async def test_soft_delete_has_history(
        self, ID1: ObjectId = ObjectId(), ID2: ObjectId = ObjectId()
    ) -> None:
        ID1 = ObjectId()
        ID2 = ObjectId()
        await self.insert_data(ID1, ID2)
        await self.crudMany.delete([str(ID1), str(ID2)])

        await self.assertChangeLogDeleteGeneral(ID1, ID2)

        assertSoftDeleteMany(
            self.crudMany,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200, HTTPCode.CODE_200],
            ["MSG_SUCCESSFULLY_SOFT_DELETED", "MSG_SUCCESSFULLY_SOFT_DELETED"],
            [[CREATE, UPDATE, DELETE], [CREATE, UPDATE, DELETE]],
        )

    async def test_soft_delete_many_check_no_data_is_retrieve_after_soft_delete(self) -> None:
        ID1 = ObjectId()
        ID2 = ObjectId()
        await self.test_soft_delete_has_history(ID1, ID2)

        entry1: TData = await self.crudMany.get_by_id(ID1)
        entry2: TData = await self.crudMany.get_by_id(ID2)

        assert not bool(entry1)
        assert not bool(entry2)

    async def assertChangeLogDeleteGeneral(self, ID1: ObjectId, ID2: ObjectId) -> None:
        self.crudMany.set_collection(collection.CHANGELOG)
        listChangelog_id1: List[TData] = await self.crudMany.get(**{"parentID": str(ID1)})
        listChangelog_id2: List[TData] = await self.crudMany.get(**{"parentID": str(ID2)})

        assertChangeLogDelete(listChangelog_id1, "2")
        assertChangeLogDelete(listChangelog_id2, "5")

    async def insert_data(self, ID1: ObjectId = ObjectId(), ID2: ObjectId = ObjectId()) -> None:
        entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
        await self.crudMany.insert_update(entries)

        entries[0]["one"] = 2
        entries[1]["one"] = 5
        await self.crudMany.insert_update(entries)


class TestCRUD_Hard_Delete_Many:
    crudMany: CrudMany = CrudMany(mongo_db)
    crudMany.set_collection(collection.CRUD)
    crudMany.options.set_softDelete(False)

    async def test_hard_delete(
        self, ID1: ObjectId = ObjectId(), ID2: ObjectId = ObjectId()
    ) -> None:
        self.crudMany.options.softDelete = False
        ID1 = ObjectId()
        ID2 = ObjectId()
        await self.insert_data(ID1, ID2)
        await self.crudMany.delete([str(ID1), str(ID2)])

        assertHardDeleteMany(
            self.crudMany,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200, HTTPCode.CODE_200],
            ["MSG_SUCCESSFULLY_HARD_DELETED", "MSG_SUCCESSFULLY_HARD_DELETED"],
        )

        assert (
            tr.translate("MSG_SUCCESSFULLY_HARD_DELETED")[:-2] in self.crudMany.get_messages()[0]
        )

    async def test_hard_delete_one_ok_other_unexisting(self) -> None:
        ID1: ObjectId = ObjectId()
        entries: List[TData] = [{"_id": ID1, "one": 1}]
        await self.crudMany.insert_update(entries)
        await self.crudMany.delete([str(ID1), str(ObjectId())])

        assertHardDeleteMany(
            self.crudMany,
            HTTPCode.CODE_400,
            [HTTPCode.CODE_200, HTTPCode.CODE_400],
            ["MSG_SUCCESSFULLY_HARD_DELETED"],
        )
        assert len(self.crudMany.get_errors()) == 1
        assert self.crudMany.get_errors()[0] == tr.translate("ERROR_UNEXISTING_DATA")

    async def test_hard_delete_has_history(
        self, ID1: ObjectId = ObjectId(), ID2: ObjectId = ObjectId()
    ) -> None:
        ID1 = ObjectId()
        ID2 = ObjectId()
        await self.insert_data(ID1, ID2)
        await self.crudMany.delete([str(ID1), str(ID2)])

        await self.assertChangeLogDeleteGeneral(ID1, ID2)

        assertHardDeleteMany(
            self.crudMany,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200, HTTPCode.CODE_200],
            ["MSG_SUCCESSFULLY_HARD_DELETED", "MSG_SUCCESSFULLY_HARD_DELETED"],
        )

    async def test_hard_delete_many_check_no_data_is_retrieve_after_hard_delete(self) -> None:
        ID1 = ObjectId()
        ID2 = ObjectId()
        self.crudMany.collection = collection.CRUD
        await self.test_hard_delete_has_history(ID1, ID2)

        entry1: TData = await self.crudMany.get_by_id(ID1)
        entry2: TData = await self.crudMany.get_by_id(ID2)

        assert not bool(entry1)
        assert not bool(entry2)

    async def assertChangeLogDeleteGeneral(self, ID1: ObjectId, ID2: ObjectId) -> None:
        self.crudMany.set_collection(collection.CHANGELOG)
        listChangelog_id1: List[TData] = await self.crudMany.get(**{"parentID": str(ID1)})
        listChangelog_id2: List[TData] = await self.crudMany.get(**{"parentID": str(ID2)})

        assertChangeLogDelete(listChangelog_id1, "2")
        assertChangeLogDelete(listChangelog_id2, "5")

    async def insert_data(self, ID1: ObjectId = ObjectId(), ID2: ObjectId = ObjectId()) -> None:
        entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
        await self.crudMany.insert_update(entries)

        entries[0]["one"] = 2
        entries[1]["one"] = 5
        await self.crudMany.insert_update(entries)


def assertChangeLogDelete(changelogs: List[TData], newValue: str) -> None:
    assert len(changelogs) == 3
    assert changelogs[0]["changeLog"] == []
    assert changelogs[1]["changeLog"][0]["field"] == "one"
    assert changelogs[1]["changeLog"][0]["oldValue"] == "1"
    assert changelogs[1]["changeLog"][0]["newValue"] == newValue
    assert changelogs[2]["changeLog"] == []


def assertSoftDeleteMany(
    crud: CrudMany,
    httpCode: HTTPCode,
    httpCodes: List[HTTPCode],
    messages: List[str],
    auditFields: List[List[str]],
) -> None:
    assertComonUpdateMany(crud, httpCode, httpCodes)
    for idx, modifiedData in enumerate(crud.get_data()):
        assertAuditFieldsUpdateMany(modifiedData, auditFields[idx])
    for idx, message in enumerate(messages):
        assertMessageUpdateMany(crud.get_messages()[idx], message)


def assertHardDeleteMany(
    crud: CrudMany,
    httpCode: HTTPCode,
    httpCodes: List[HTTPCode],
    messages: List[str],
) -> None:
    assertComonUpdateMany(crud, httpCode, httpCodes)
    for idx, message in enumerate(messages):
        assertMessageUpdateMany(crud.get_messages()[idx], message)


def assertComonUpdateMany(crud: CrudMany, httpCode: HTTPCode, httpCodes: List[HTTPCode]) -> None:
    assert crud.http_code == httpCode
    assert crud.http_codes == httpCodes


def assertAuditFieldsUpdateMany(modifiedData: TData, auditFields: List[str]) -> None:
    if CREATE in auditFields:
        assert CREATE_DATE in modifiedData
        assert CREATE_USER in modifiedData
    else:
        assert CREATE_DATE not in modifiedData
        assert CREATE_USER not in modifiedData
    if UPDATE in auditFields:
        assert MODIFIED_DATE in modifiedData
        assert MODIFIED_USER in modifiedData
    else:
        assert MODIFIED_DATE not in modifiedData
        assert MODIFIED_USER not in modifiedData
    if DELETE in auditFields:
        assert DELETED_DATE in modifiedData
        assert DELETED_USER in modifiedData
    else:
        assert DELETED_DATE not in modifiedData
        assert DELETED_USER not in modifiedData


def assertMessageUpdateMany(savedMessage: str, message: str) -> None:
    assert tr.translate(message)[:-2] in savedMessage


def assertChangelog_soft_delete_after_insert(listChangelog: List[TData]) -> None:
    for changelog in listChangelog:
        if changelog["action"] in [CREATE, DELETE]:
            assert changelog[collection.CHANGELOG] == []


async def update_entry(
    crudMany: CrudMany, ID1: ObjectId = ObjectId(), ID2: ObjectId = ObjectId()
) -> None:
    entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
    await crudMany.insert_update(entries)
    entries = crudMany.get_data()
    entries[0]["one"] = 2
    entries[1]["one"] = 5
    await crudMany.insert_update(entries)


def assert_hard_delete_after_insert(crudMany: CrudMany) -> None:
    data: TData = crudMany.get_data()
    assert_hard_delete_after_insert_only_data(data)


def assert_hard_delete_after_insert_only_data(data: TData) -> None:
    assert CREATE_DATE in data
    assert CREATE_USER in data
    assert MODIFIED_DATE not in data
    assert MODIFIED_USER not in data
    assert DELETED_DATE not in data
    assert DELETED_USER not in data


def assert_delete_after_insert(crudMany: CrudMany) -> None:
    data: TData = crudMany.get_data()
    assert_soft_delete_after_insert_only_data(data)


def assert_soft_delete_after_insert_only_data(data: TData) -> None:
    assert CREATE_DATE in data
    assert CREATE_USER in data
    assert MODIFIED_DATE not in data
    assert MODIFIED_USER not in data
    assert DELETED_DATE in data
    assert DELETED_USER in data


def assert_hard_delete_after_update(crudMany: CrudMany) -> None:
    data: TData = crudMany.get_data()
    assert_hard_delete_after_update_only_data(data)


def assert_hard_delete_after_update_only_data(data: TData) -> None:
    assert CREATE_DATE in data
    assert CREATE_USER in data
    assert MODIFIED_DATE in data
    assert MODIFIED_USER in data
    assert DELETED_DATE not in data
    assert DELETED_USER not in data


def assert_soft_delete_after_update(crudMany: CrudMany) -> None:
    data: TData = crudMany.get_data()
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


async def insert_one_by_id(id: str, crudMany: CrudMany, **additionalData: Dict) -> TData:
    entries: List[TData] = [{"_id": ObjectId(id), "one": 1, **additionalData}]
    await crudMany.insert_update(entries)
    return crudMany.get_data()


def assertCreateCrudOptions(optCrud: CrudOptions) -> None:
    assert optCrud.projectId == PROJECT_ID
    assert optCrud.userId == USER
    assert optCrud.actionChangeLog == "Update"
    assert optCrud.omitFields == OMIT_FIELDS
    assert optCrud.updateAuditFields is True
    assert optCrud.updateChangeLog is True
    assert optCrud.softDelete is True
    assert optCrud.filterByUser is False


def assertErrorInsertOne(crudMany: CrudMany, excinfo: Any) -> None:
    assert not bool(crudMany.get_message())
    assert not bool(crudMany.get_data())
    assert bool(crudMany.get_error())
    assert crudMany.get_error() == str(excinfo.value)


def assertErrorDelete(
    crudMany: CrudMany, excinfo: Any, http_code: HTTPCode = HTTPCode.CODE_400
) -> None:
    assert not bool(crudMany.get_message())
    assert not bool(crudMany.get_data())
    assert bool(crudMany.get_error())
    assert crudMany.get_error() == str(excinfo.value)
    assert crudMany.http_code == http_code


def assertCreateCRUDObject(crudMany: CrudMany) -> None:
    assert isinstance(crudMany.mongoDB, Database)
    assert isinstance(crudMany.message, List)
    assert isinstance(crudMany.data, List)


def assertMessage(returnedMessage: str, msg: str, lang: str = "en") -> None:
    assert tr.translate(msg, lang)[:30] in returnedMessage
