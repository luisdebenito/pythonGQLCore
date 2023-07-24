import os
import sys
from typing import Any, Dict, List

import pytest
from bson import ObjectId

from conftest import mongo_db

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.http_codes import HTTPCode
from _python_core.crud.crud_constants import (
    OMIT_FIELDS,
    CREATE,
    UPDATE,
    DELETE,
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

# Kurt USERID
USER = "02477c69-56f4-4e77-921a-23a2a82a335e"
PROJECT_ID = "12070c789f30472094bbcf61923ecab4"


class collection:
    CRUD = "crud"
    CHANGELOG = "changeLog"


class TestCRUD_InsertMany:
    crudMany: CrudMany = CrudMany(mongo_db)
    crudMany.set_collection(collection.CRUD)

    async def test_insert_error_before_processing_individual_schemas(self) -> None:
        entries: List[TData] = []
        await self.crudMany.insert_update(entries)

        assertErrorInsertMany(self.crudMany, HTTPCode.CODE_400)
        assert len(self.crudMany.get_errors()) == 1
        assert self.crudMany.get_errors()[0] == tr.translate("ERROR_EMPTY_SCHEMA")
        assert self.crudMany.http_codes == []

    async def test_insert_error_empty_schema(self) -> None:
        entries: List[TData] = [{}]
        await self.crudMany.insert_update(entries)

        assertErrorInsertMany(self.crudMany, HTTPCode.CODE_400)
        assert len(self.crudMany.get_errors()) == 1
        assert self.crudMany.get_errors()[0] == tr.translate("ERROR_EMPTY_SCHEMA")
        assert self.crudMany.http_codes == [HTTPCode.CODE_400]

    async def test_insert_error_in_one_schema_when_one_schema_is_provided(self) -> None:
        entries: List[TData] = [{"id": 1, "code": "Invalid ID"}]
        await self.crudMany.insert_update(entries)

        assertErrorInsertMany(self.crudMany, HTTPCode.CODE_400)
        assert len(self.crudMany.get_errors()) == 1
        assert tr.translate("ERROR_INVALID_ID")[:-2] in self.crudMany.get_errors()[0]
        assert self.crudMany.http_codes == [HTTPCode.CODE_400]

    async def test_insert_valid_data_without_id(self) -> None:
        entries: List[TData] = [{"one": 1}]
        await self.crudMany.insert_update(entries)

        assertInsertMany(self.crudMany)
        assert len(self.crudMany.get_messages()) == 1
        assert tr.translate("MSG_SUCCESSFULLY_INSERTED")[:-2] in self.crudMany.get_messages()[0]
        assert self.crudMany.http_codes == [HTTPCode.CODE_200]

    async def test_insert_valid_data_with_id_null(self) -> None:
        entries: List[TData] = [{"id": None, "one": 1}]
        await self.crudMany.insert_update(entries)

        assertInsertMany(self.crudMany)
        assert len(self.crudMany.get_messages()) == 1
        assert tr.translate("MSG_SUCCESSFULLY_INSERTED")[:-2] in self.crudMany.get_messages()[0]
        assert self.crudMany.http_codes == [HTTPCode.CODE_200]

    async def test_schemas_are_deleted_after_inserting(self) -> None:
        entries: List[TData] = [{"id": None, "one": 1}]
        await self.crudMany.insert_update(entries)

        assert self.crudMany.schemas == []

    async def test_insert_two_valid_schemas(self) -> None:
        entries: List[TData] = [{"one": 1}, {"two": 2}]
        await self.crudMany.insert_update(entries)

        assertInsertMany(self.crudMany)
        assert len(self.crudMany.get_messages()) == 2
        assert tr.translate("MSG_SUCCESSFULLY_INSERTED")[:-2] in self.crudMany.get_messages()[0]
        assert tr.translate("MSG_SUCCESSFULLY_INSERTED")[:-2] in self.crudMany.get_messages()[1]
        assert self.crudMany.http_codes == [HTTPCode.CODE_200, HTTPCode.CODE_200]


class TestCRUD_UpdateMany:
    crudMany: CrudMany = CrudMany(mongo_db)
    crudMany.set_collection(collection.CRUD)

    async def test_update_with_ObjectId(
        self, ID1: ObjectId = ObjectId(), ID2: ObjectId = ObjectId()
    ) -> None:
        self.crudMany.collection = collection.CRUD
        entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
        await self.crudMany.insert_update(entries)

        entries[0]["one"] = 2
        entries[1]["one"] = 5
        await self.crudMany.insert_update(entries)

        assertUpdateMany(
            self.crudMany,
            entries,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200, HTTPCode.CODE_200],
            ["MSG_SUCCESSFULLY_UPDATED", "MSG_SUCCESSFULLY_UPDATED"],
            [[CREATE, UPDATE], [CREATE, UPDATE]],
        )

    async def test_update_no_changes(self) -> None:
        ID1: ObjectId = ObjectId()
        ID2: ObjectId = ObjectId()
        entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
        await self.crudMany.insert_update(entries)
        await self.crudMany.insert_update(entries)

        assertUpdateMany(
            self.crudMany,
            entries,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200, HTTPCode.CODE_200],
            ["MESSAGE_NO_CHANGES_TO_UPDATE", "MESSAGE_NO_CHANGES_TO_UPDATE"],
            [[CREATE], [CREATE]],
        )

    async def test_update_two_and_second_without_changes(self) -> None:
        ID1: ObjectId = ObjectId()
        ID2: ObjectId = ObjectId()
        entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
        await self.crudMany.insert_update(entries)
        entries[0]["one"] = 4
        await self.crudMany.insert_update(entries)

        assertUpdateMany(
            self.crudMany,
            entries,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200, HTTPCode.CODE_200],
            ["MSG_SUCCESSFULLY_UPDATED", "MESSAGE_NO_CHANGES_TO_UPDATE"],
            [[CREATE, UPDATE], [CREATE]],
        )

    async def test_update_two_and_first_without_changes(self) -> None:
        ID1: ObjectId = ObjectId()
        ID2: ObjectId = ObjectId()
        entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
        await self.crudMany.insert_update(entries)
        entries[-1]["one"] = 4
        await self.crudMany.insert_update(entries)

        assertUpdateMany(
            self.crudMany,
            entries,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200, HTTPCode.CODE_200],
            ["MESSAGE_NO_CHANGES_TO_UPDATE", "MSG_SUCCESSFULLY_UPDATED"],
            [[CREATE], [CREATE, UPDATE]],
        )

    async def test_update_empty_entries(self) -> None:
        ID1: ObjectId = ObjectId()
        ID2: ObjectId = ObjectId()
        entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
        emptyEntries: List[TData] = []
        await self.crudMany.insert_update(entries)
        await self.crudMany.insert_update(emptyEntries)

        assertUpdateErrorMany(self.crudMany, HTTPCode.CODE_400)
        assert len(self.crudMany.errors) == 1
        assert self.crudMany.get_errors()[0] == tr.translate("ERROR_EMPTY_SCHEMA")

    async def test_update_update_first_ok_second_error(self) -> None:
        ID1: ObjectId = ObjectId()
        ID2: ObjectId = ObjectId()
        entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
        await self.crudMany.insert_update(entries)
        entries[-1] = {}
        await self.crudMany.insert_update(entries)

        assertUpdateMany(
            self.crudMany,
            entries,
            HTTPCode.CODE_400,
            [HTTPCode.CODE_200, HTTPCode.CODE_400],
            ["MESSAGE_NO_CHANGES_TO_UPDATE"],
            [[CREATE]],
        )
        assert len(self.crudMany.errors) == 1
        assert self.crudMany.get_errors()[0] == tr.translate("ERROR_EMPTY_SCHEMA")

    async def test_update_update_both_with_error(self) -> None:
        ID1: ObjectId = ObjectId()
        ID2: ObjectId = ObjectId()
        entries: List[TData] = [{"_id": ID1, "one": 1}, {"_id": ID2, "one": 1}]
        await self.crudMany.insert_update(entries)
        entries[0] = {}
        entries[-1] = {}
        await self.crudMany.insert_update(entries)

        assertUpdateMany(
            self.crudMany,
            entries,
            HTTPCode.CODE_400,
            [HTTPCode.CODE_400, HTTPCode.CODE_400],
            [],
            [],
        )
        assert len(self.crudMany.errors) == 2
        assert self.crudMany.get_errors()[0] == tr.translate("ERROR_EMPTY_SCHEMA")
        assert self.crudMany.get_errors()[1] == tr.translate("ERROR_EMPTY_SCHEMA")

    async def test_update_two_has_history(self) -> None:
        ID1: ObjectId = ObjectId()
        ID2: ObjectId = ObjectId()
        await self.test_update_with_ObjectId(ID1, ID2)

        self.crudMany.set_collection(collection.CHANGELOG)
        listChangelog_id1: List[TData] = await self.crudMany.get(**{"parentID": str(ID1)})
        listChangelog_id2: List[TData] = await self.crudMany.get(**{"parentID": str(ID2)})

        assertChangeLogUpdate2(listChangelog_id1, "2")
        assertChangeLogUpdate2(listChangelog_id2, "5")


def assertChangeLogUpdate2(changelogs: List[TData], newValue: str) -> None:
    assert len(changelogs) == 2
    assert changelogs[1]["changeLog"] == []
    assert changelogs[0]["changeLog"][0]["field"] == "one"
    assert changelogs[0]["changeLog"][0]["oldValue"] == "1"
    assert changelogs[0]["changeLog"][0]["newValue"] == newValue


def assertInsertMany(crudMany: CrudMany) -> None:
    assert crudMany.http_code == HTTPCode.CODE_200
    assert bool(crudMany.get_messages())
    assert bool(crudMany.get_data())
    assert not bool(crudMany.get_errors())


def assertErrorInsertMany(crudMany: CrudMany, http_code: HTTPCode = HTTPCode.CODE_400) -> None:
    assert crudMany.http_code == http_code
    assert not bool(crudMany.get_messages())
    assert not bool(crudMany.get_data())
    assert bool(crudMany.get_errors())


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


def assertCreateCrudOptions(optCrud: CrudOptions) -> None:
    assert optCrud.projectId == PROJECT_ID
    assert optCrud.userId == USER
    assert optCrud.actionChangeLog == "Update"
    assert optCrud.omitFields == OMIT_FIELDS
    assert optCrud.updateAuditFields is True
    assert optCrud.updateChangeLog is True
    assert optCrud.softDelete is True
    assert optCrud.filterByUser is False


def assertUpdateMany(
    crud: CrudMany,
    entries: List[TData],
    httpCode: HTTPCode,
    httpCodes: List[HTTPCode],
    messages: List[str],
    auditFields: List[List[str]],
) -> None:
    assertComonUpdateMany(crud, entries, httpCode, httpCodes)
    for idx, modifiedData in enumerate(crud.get_data()):
        assertAuditFieldsUpdateMany(modifiedData, auditFields[idx])
    for idx, message in enumerate(messages):
        assertMessageUpdateMany(crud.get_messages()[idx], message)


def assertUpdateErrorMany(crud: CrudMany, httpCode: HTTPCode) -> None:
    assert crud.http_code == httpCode
    assert not bool(crud.get_messages())
    assert not bool(crud.get_data())


def assertMessageUpdateMany(savedMessage: str, message: str) -> None:
    assert tr.translate(message)[:-2] in savedMessage


def assertComonUpdateMany(
    crud: CrudMany, entries: List[TData], httpCode: HTTPCode, httpCodes: List[HTTPCode]
) -> None:
    assert crud.http_code == httpCode
    assert crud.http_codes == httpCodes
    assert len(entries) == len(crud.get_messages()) + len(crud.get_errors())


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


def assertData(listSchemas: List[TData], schema: TData) -> None:
    for elm in schema:
        if elm in OMIT_FIELDS:
            continue
        assert schema[elm] == listSchemas[0][elm]


def assertMessage(listMessages: List[str], msg: str, lang: str = "en") -> None:
    assert tr.translate(msg, lang)[:30] in listMessages[0]
