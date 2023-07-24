from datetime import datetime
import os
import sys
from typing import Any, Dict, List
from _python_core.constants import DATETIME

import pytest

if os.getenv("MOCK_TEST") == "True":
    from mongomock import Database
else:
    from pymongo.database import Database

from bson import ObjectId

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))
from _python_core.crud.crud_constants import (
    MAXDATE,
    MINDATE,
    NAME,
    OMIT_FIELDS,
    CREATE_DATE,
    CREATE_USER,
    DELETED_DATE,
    DELETED_USER,
    MODIFIED_DATE,
    MODIFIED_USER,
    REQUESTDATE,
)
from _python_core.Errors import ErrorBase
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


class TestCrudOptions:
    optCrud: CrudOptions = CrudOptions(PROJECT_ID, USER)

    def test_object(self) -> Any:
        assertCreateCrudOptions(self.optCrud)

    def test_object_create_with_no_arguments(self) -> Any:
        optCrud = CrudOptions()
        assert optCrud.projectId == ""
        assert optCrud.userId == ""
        assert optCrud.actionChangeLog == "Update"
        assert optCrud.omitFields == OMIT_FIELDS
        assert optCrud.updateAuditFields is True
        assert optCrud.updateChangeLog is True
        assert optCrud.softDelete is True
        assert optCrud.filterByUser is False

    def test_object_actionChange_create(self) -> Any:
        self.optCrud.set_actionChangeLog("Create")
        assert self.optCrud.actionChangeLog == "Create"

    def test_object_actionChange_delete(self) -> Any:
        self.optCrud.set_actionChangeLog("Delete")
        assert self.optCrud.actionChangeLog == "Delete"

    def test_object_skip_delete_entries(self) -> Any:
        self.optCrud.set_skipDeletedEntries(False)
        assert self.optCrud.skipDeletedEntries is False

    def test_object_skip_inactive_entries(self) -> Any:
        self.optCrud.set_skipInactiveEntries(True)
        assert self.optCrud.skipInactiveEntries is True

    def test_object_filter_by_user(self) -> Any:
        self.optCrud.set_filterByUser(True)
        assert self.optCrud.filterByUser is True

    def test_object_date_filter_enabled(self) -> Any:
        self.optCrud.set_dateFilter(
            {
                NAME: "somePathToDate",
                REQUESTDATE: datetime.now(),
            }
        )
        assert self.optCrud._is_date_filter_enabled() is True

    def test_object_Wrong_actionChange(self) -> Any:
        with pytest.raises(ErrorBase) as excinfo:
            self.optCrud.set_actionChangeLog("Test")
        assert tr.translate("ERROR_WRONG_ACTION_CHANGELOG") == str(excinfo.value)

    def test_object_Wrong_actionChange_language(self) -> Any:
        lang: str = "es"
        self.optCrud.set_language(lang)
        with pytest.raises(ErrorBase) as excinfo:
            self.optCrud.set_actionChangeLog("Test")
        assert tr.translate("ERROR_WRONG_ACTION_CHANGELOG", lang) == str(excinfo.value)

    def test_object_create_fromGraphQL(self) -> Any:
        crudOptions = {
            "softDelete": False,
            "dateFilter": {
                MAXDATE: "2023-02-06T00:00:00.000Z",
                "name": "whatever",
            },
        }
        self.optCrud.set_optionsFromGQL(**crudOptions)
        assert self.optCrud.softDelete is False
        assert self.optCrud.skipDeletedEntries is True

    def test_set_additionalFilter(self) -> Any:
        crudOptions = {
            "additional_filter": '{"a":1}',
            "dateFilter": {
                MAXDATE: "2023-02-06T00:00:00.000Z",
                "name": "whatever",
            },
        }
        self.optCrud.set_optionsFromGQL(**crudOptions)
        assert self.optCrud.additionalFilter == {"a": 1}

    def test_dontset_additionalFilter_when_crudOptions_none(self) -> Any:
        crudOptions: Dict = {
            "dateFilter": {
                MAXDATE: "2023-02-06T00:00:00.000Z",
                "name": "whatever",
            },
        }
        self.optCrud.set_optionsFromGQL(**crudOptions)
        assert self.optCrud.additionalFilter == {}

    def test_projection_is_empty(self) -> None:
        crudOptions: Dict = {
            "dateFilter": {
                MAXDATE: "2023-02-06T00:00:00.000Z",
                "name": "whatever",
            },
        }
        self.optCrud.set_optionsFromGQL(**crudOptions)
        assert not self.optCrud.projection

    def test_projection_ok_from_setoptionsFromGQL(self) -> None:
        crudOptions: Dict = {
            "projection": {"ok": 1},
            "dateFilter": {
                MAXDATE: "2023-02-06T00:00:00.000Z",
                "name": "whatever",
            },
        }
        self.optCrud.set_optionsFromGQL(**crudOptions)
        assert len(self.optCrud.projection.keys())

    def test_projection_of_from_set_projection(self) -> None:
        crudOptions: Dict = {
            "dateFilter": {
                MAXDATE: "2023-02-06T00:00:00.000Z",
                "name": "whatever",
            },
        }
        self.optCrud.set_optionsFromGQL(**crudOptions)
        self.optCrud.set_projection({"ok": 1})
        assert len(self.optCrud.projection.keys())

    def test_projection_of_from_set_sort(self) -> None:
        crudOptions: Dict = {
            "dateFilter": {
                MAXDATE: "2023-02-06T00:00:00.000Z",
                "name": "whatever",
            },
        }
        self.optCrud.set_optionsFromGQL(**crudOptions)
        self.optCrud.set_sort([({"_id", 1})])
        assert len(self.optCrud.sort)

    def test_ok_noDateFilter(self) -> None:
        optCrud = CrudOptions()
        _crudOptions: Dict = {}
        optCrud.set_optionsFromGQL(**_crudOptions)
        assert not optCrud.dateFilter[MAXDATE]
        assert not optCrud.dateFilter[MINDATE]
        assert not optCrud.dateFilter[REQUESTDATE]

    def test_ok_DateFilter_no_name(self) -> None:
        optCrud = CrudOptions()
        _crudOptions: Dict = {
            "dateFilter": {
                MAXDATE: "2023-02-06T00:00:00.000Z",
            },
        }
        optCrud.set_optionsFromGQL(**_crudOptions)
        assert optCrud.dateFilter[MAXDATE]

    def test_ok_DateFilter_date(self) -> None:
        optCrud = CrudOptions()
        _crudOptions: Dict = {
            "dateFilter": {
                MAXDATE: datetime.now().strftime(DATETIME),
            },
        }
        optCrud.set_optionsFromGQL(**_crudOptions)
        assert optCrud.dateFilter[MAXDATE]
        assert optCrud.dateFilter[NAME] == CREATE_DATE

    def test_ok_DateFilter_date_from_str(self) -> None:
        crudOptions: Dict = {
            "dateFilter": {
                MAXDATE: "2023-02-06T00:00:00.000Z",
                "name": "whatever",
            },
        }
        self.optCrud.set_optionsFromGQL(**crudOptions)
        assert isinstance(self.optCrud.dateFilter[MAXDATE], datetime)


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


def assertErrorInsertOne(crud: CrudOne, excinfo: Any) -> None:
    assert bool(crud.get_messages())
    assert bool(crud.get_data()) is False
    assert crud.get_messages()[0] == str(excinfo.value)


def assertErrorDelete(crud: CrudOne, excinfo: Any) -> None:
    assert bool(crud.get_messages())
    assert bool(crud.get_data()) is False
    assert crud.get_messages()[0] == str(excinfo.value)


def assertCreateCRUDObject(crud: CrudOne) -> None:
    assert isinstance(crud.mongoDB, Database)
    assert isinstance(crud.messages, List)
    assert isinstance(crud.data, List)


def assertInsert(crud: CrudOne, entry: TData, msg: str) -> None:
    assert bool(crud.get_messages())
    assert bool(crud.get_data())
    assertData(crud.get_data(), entry)
    assertMessage(crud.get_messages(), msg, crud.lang)
    assert CREATE_DATE in crud.get_data()[0]
    assert CREATE_USER in crud.get_data()[0]
    assert MODIFIED_USER not in crud.get_data()[0]
    assert MODIFIED_DATE not in crud.get_data()[0]


def assertUpdate(crud: CrudOne, entry: TData, msg: str) -> None:
    assert bool(crud.get_messages())
    assert bool(crud.get_data())
    assertData(crud.get_data(), entry)
    assertMessage(crud.get_messages(), msg, crud.lang)
    assert CREATE_DATE in crud.get_data()[0]
    assert CREATE_USER in crud.get_data()[0]
    assert MODIFIED_USER in crud.get_data()[0]
    assert MODIFIED_DATE in crud.get_data()[0]


def assertSoftDelete(crud: CrudOne, entry: TData, msg: str) -> None:
    assert bool(crud.get_messages())
    assert bool(crud.get_data())
    assertData(crud.get_data(), entry)
    assertMessage(crud.get_messages(), msg, crud.lang)
    assert CREATE_DATE in crud.get_data()[0]
    assert CREATE_USER in crud.get_data()[0]
    assert DELETED_DATE in crud.get_data()[0]
    assert DELETED_USER in crud.get_data()[0]


def assertData(listSchemas: List[TData], schema: TData) -> None:
    for elm in schema:
        if elm in OMIT_FIELDS:
            continue
        assert schema[elm] == listSchemas[0][elm]


def assertMessage(listMessages: List[str], msg: str, lang: str = "en") -> None:
    assert tr.translate(msg, lang)[:30] in listMessages[0]
