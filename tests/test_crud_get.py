from datetime import datetime, timedelta
import os
import sys
import random
from typing import Any, Dict, List

import pytest
from pymongo import ASCENDING

if os.getenv("MOCK_TEST") == "True":
    from mongomock import Database
else:
    from pymongo.database import Database

from bson import ObjectId

from conftest import mongo_db

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.crud.crud_constants import (
    MAXDATE,
    MINDATE,
    NAME,
    OMIT_FIELDS,
    CREATE_USER,
    CREATE_DATE,
    DELETED_DATE,
    DELETED_USER,
    MODIFIED_DATE,
    MODIFIED_USER,
    REQUESTDATE,
)
from _python_core.crud.crud_single import CrudOne
from _python_core.crud.crud_options import CrudOptions
from _python_core.translations import Translations as tr
from _python_core import Errors as err

TData = Dict[str, Any]  # Type object as defined in GQL Schema

# Kurt USERID
USER = "02477c69-56f4-4e77-921a-23a2a82a335e"
PROJECT_ID = "12070c789f30472094bbcf61923ecab4"


class collection:
    CRUD = "crud"
    CRUD_PAGINATION = "pagination"
    CHANGELOG = "changeLog"


class TestCrudGetByID:
    crud: CrudOne = CrudOne(mongo_db)
    crud.set_collection(collection.CRUD)

    async def test_get_by_id(self) -> None:
        ID: str = str(ObjectId())
        createdData: TData = await insert_one_by_id(ID, self.crud)
        retrievedData: TData = await self.crud.get_by_id(ID)

        assert_createdData_equals_retievedData(createdData, retrievedData)

    async def test_get_by_id_no_data_returned(self) -> None:
        ID: str = str(ObjectId())
        retrievedData: TData = await self.crud.get_by_id(ID)

        assert not bool(retrievedData)

    async def test_get_by_id_wrong_id(self) -> None:
        ID: str = "WrongID"
        data: TData = await self.crud.get_by_id(ID)

        assert not bool(data)


class TestCrudGetSingle:
    crud: CrudOne = CrudOne(mongo_db)
    crud.set_collection(collection.CRUD)

    async def test_get_single(self) -> None:
        ID: ObjectId = ObjectId()
        _filter: Dict = {"_id": ID}
        createdData: TData = await insert_one_by_id(str(ID), self.crud)
        retrievedData: TData = await self.crud.get_single(**_filter)

        assert_createdData_equals_retievedData(createdData, retrievedData)

    async def test_get_single_no_data_returned(self) -> None:
        ID: ObjectId = ObjectId()
        _filter: Dict = {"_id": ID}
        retrievedData: TData = await self.crud.get_single(**_filter)

        assert not bool(retrievedData)

    async def test_get_single_with_sort(self) -> None:
        ID1 = ObjectId()
        ID2 = ObjectId()
        ID3 = ObjectId()
        data1: Dict = {"_id": ID1, "number": 1, "tag": "test_single_sort"}
        data2: Dict = {"_id": ID2, "number": 3, "tag": "test_single_sort"}
        data3: Dict = {"_id": ID3, "number": 2, "tag": "test_single_sort"}

        await self.crud.insert_update(data1)
        await self.crud.insert_update(data2)
        await self.crud.insert_update(data3)

        _sort = [("number", -1)]
        _filter = {"tag": "test_single_sort"}

        retrievedData: TData = await self.crud.get_single(_sort, **_filter)

        assert retrievedData["number"] == 3


class TestCrudGetByDates:
    async def test_get_with_date_request_day_filter(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        ID: ObjectId = ObjectId()
        _filter: Dict = {"two": "filterDate"}
        createdData: TData = await insert_one_by_id(str(ID), crud, **_filter)

        date = datetime.now()

        # Filter for today
        crud.options.set_dateFilter(
            {
                NAME: CREATE_DATE,
                REQUESTDATE: date,
            }
        )

        retrievedData: List[TData] = await crud.get(**_filter)

        assert len(retrievedData) == 1
        assert_createdData_equals_retievedData(createdData, retrievedData[0])

        # Filter for yesterday
        crud.options.set_dateFilter(
            {
                NAME: CREATE_DATE,
                REQUESTDATE: date - timedelta(days=1),
            }
        )
        retrievedData2: List[TData] = await crud.get(**_filter)

        assert len(retrievedData2) == 0

        # Filter for tomorrow
        crud.options.set_dateFilter(
            {
                NAME: CREATE_DATE,
                REQUESTDATE: date + timedelta(days=1),
            }
        )
        retrievedData3: List[TData] = await crud.get(**_filter)

        assert len(retrievedData3) == 0

    async def test_get_with_date_range_filter(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        ID: ObjectId = ObjectId()
        _filter: Dict = {"two": "rangeDate"}
        createdData: TData = await insert_one_by_id(str(ID), crud, **_filter)  # type: ignore
        date = datetime.now()

        crud.options.set_dateFilter(
            {
                NAME: CREATE_DATE,
                MINDATE: date - timedelta(days=1),
                MAXDATE: date + timedelta(days=1),
            }
        )

        retrievedData: List[TData] = await crud.get(**_filter)

        assert len(retrievedData) == 1
        assert_createdData_equals_retievedData(createdData, retrievedData[0])

        # Filter a non valid range
        crud.options.set_dateFilter(
            {
                NAME: CREATE_DATE,
                MINDATE: date + timedelta(days=1),
                MAXDATE: date + timedelta(days=2),
            }
        )
        retrievedData2: List[TData] = await crud.get(**_filter)

        assert len(retrievedData2) == 0

    async def test_get_with_min_date(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        ID: ObjectId = ObjectId()
        _filter: Dict = {"two": "minDate"}
        createdData: TData = await insert_one_by_id(str(ID), crud, **_filter)  # type: ignore

        date = datetime.now()

        crud.options.set_dateFilter(
            {
                NAME: CREATE_DATE,
                MINDATE: date - timedelta(days=1),
            }
        )

        retrievedData: List[TData] = await crud.get(**_filter)

        assert len(retrievedData) == 1
        assert_createdData_equals_retievedData(createdData, retrievedData[0])

        crud.options.set_dateFilter(
            {
                NAME: CREATE_DATE,
                MINDATE: date + timedelta(days=1),
            }
        )
        retrievedData2: List[TData] = await crud.get(**_filter)

        assert len(retrievedData2) == 0

    async def test_get_with_max_date(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        ID: ObjectId = ObjectId()
        _filter: Dict = {"two": "maxDate"}
        createdData: TData = await insert_one_by_id(str(ID), crud, **_filter)  # type: ignore

        date = datetime.now()

        crud.options.set_dateFilter(
            {
                NAME: CREATE_DATE,
                MAXDATE: date + timedelta(days=1),
            }
        )

        retrievedData: List[TData] = await crud.get(**_filter)

        assert len(retrievedData) == 1
        assert_createdData_equals_retievedData(createdData, retrievedData[0])

        # Filter a non valid max
        crud.options.set_dateFilter(
            {
                NAME: CREATE_DATE,
                MAXDATE: date - timedelta(days=1),
            }
        )
        retrievedData2: List[TData] = await crud.get(**_filter)

        assert len(retrievedData2) == 0

    async def test_set_worng_date_filter(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        crud.options.set_dateFilter(
            {
                NAME: CREATE_DATE,
            }
        )
        assert not crud.options.dateFilter[MAXDATE]
        assert not crud.options.dateFilter[MINDATE]
        assert not crud.options.dateFilter[REQUESTDATE]


class TestCrudGetActives:
    async def test_get_with_active_filter(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        _filter: Dict = {"two": "activeFilter"}
        ID1: ObjectId = ObjectId()
        await insert_one_by_id(str(ID1), crud, **{"active": True, **_filter})  # type: ignore
        ID2: ObjectId = ObjectId()
        await insert_one_by_id(str(ID2), crud, **{"active": False, **_filter})  # type: ignore

        crud.options.set_skipInactiveEntries(True)
        retrievedData: List[TData] = await crud.get(**_filter)

        assert len(retrievedData) == 1

        assert retrievedData[0].get("active") is True

        crud.options.set_skipInactiveEntries(False)

        retrievedData2: List[TData] = await crud.get(**_filter)

        assert len(retrievedData2) == 2

    async def test_get_with_additional_filter(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        _filter: Dict = {"two": "activeFilter"}
        ID1: ObjectId = ObjectId()
        await insert_one_by_id(str(ID1), crud, **{"filter1": True, **_filter})  # type: ignore
        ID2: ObjectId = ObjectId()
        await insert_one_by_id(str(ID2), crud, **{"filter1": False, **_filter})  # type: ignore

        crud.options.additionalFilter = {"filter1": False}
        retrievedData: List[TData] = await crud.get()
        assert len(retrievedData) == 1


class TestCrudGetDeleted:
    async def test_get_with_deleted_filter(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_collection(collection.CRUD)
        _filter: Dict = {"three": "deletedFilter"}
        ID1: ObjectId = ObjectId()
        await insert_one_by_id(str(ID1), crud, **{"deletedUser": {"id": "111"}, "deletedDate": datetime.now(), **_filter})  # type: ignore
        ID2: ObjectId = ObjectId()
        await insert_one_by_id(str(ID2), crud, **{"name": "noDeleted", **_filter})  # type: ignore

        crud.options.set_skipDeletedEntries(True)
        retrievedData: List[TData] = await crud.get(**_filter)

        assert len(retrievedData) == 1

        assert retrievedData[0].get("name") == "noDeleted"

        crud.options.set_skipDeletedEntries(False)

        retrievedData2: List[TData] = await crud.get(**_filter)

        assert len(retrievedData2) == 2


class TestCrudGetWithUserFilter:
    async def test_get_with_user_filter(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_options(CrudOptions(PROJECT_ID, USER))
        crud.set_collection(collection.CRUD)
        await crud.insert_update({CREATE_USER: {"id": USER}})

        crud.options.set_filterByUser(True)
        retrievedData: List[TData] = await crud.get()

        assert len(retrievedData) == 1

        assert retrievedData[0].get(CREATE_USER) == {"id": USER}


class TestCrudGetWitProjection:
    async def test_projection_is_None(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_options(CrudOptions(PROJECT_ID, USER))
        crud.set_collection(collection.CRUD)
        await crud.insert_update({PROJECT_ID: ObjectId(), NAME: "name"})

        retrievedData: List[TData] = await crud.get()

        assert retrievedData[0].get(NAME) == "name"
        assert retrievedData[0].get(PROJECT_ID)

    async def test_projection_only_include_name(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_options(CrudOptions(PROJECT_ID, USER))
        crud.set_collection(collection.CRUD)
        await crud.insert_update({PROJECT_ID: ObjectId(), NAME: "name"})

        crud.options.set_projection({NAME: 1})

        retrievedData: List[TData] = await crud.get()

        assert retrievedData[0].get(NAME) == "name"
        assert not retrievedData[0].get(PROJECT_ID)

    async def test_projection_only_exclude_name(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_options(CrudOptions(PROJECT_ID, USER))
        crud.set_collection(collection.CRUD)
        _id = ObjectId()
        await crud.insert_update({PROJECT_ID: _id, NAME: "name"})

        crud.options.set_projection({NAME: 0})

        retrievedData: List[TData] = await crud.get()

        assert not retrievedData[0].get(NAME)
        assert retrievedData[0].get(PROJECT_ID) == _id

    async def test_projection_include_multiple_fields(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_options(CrudOptions(PROJECT_ID, USER))
        crud.set_collection(collection.CRUD)
        _id = ObjectId()
        await crud.insert_update(
            {PROJECT_ID: _id, NAME: "name", "pe": "pa", "y": "agua", "pa": "la", "seca": 1}
        )

        crud.options.set_projection({NAME: 1, "pe": 1, "pa": 1})

        retrievedData: List[TData] = await crud.get()

        assert retrievedData[0].get(NAME)
        assert retrievedData[0].get("pe")
        assert retrievedData[0].get("pa")
        assert not retrievedData[0].get("y")
        assert not retrievedData[0].get("seca")

    async def test_projection_exclude_multiple_fields(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_options(CrudOptions(PROJECT_ID, USER))
        crud.set_collection(collection.CRUD)
        _id = ObjectId()
        await crud.insert_update(
            {PROJECT_ID: _id, NAME: "name", "pe": "pa", "y": "agua", "pa": "la", "seca": 1}
        )

        crud.options.set_projection({NAME: 0, "pe": 0, "pa": 0})

        retrievedData: List[TData] = await crud.get()

        assert not retrievedData[0].get(NAME)
        assert not retrievedData[0].get("pe")
        assert not retrievedData[0].get("pa")
        assert retrievedData[0].get("y")
        assert retrievedData[0].get("seca")

    async def test_projection_exclude_some_include_some_fields_error(self) -> None:
        crud: CrudOne = CrudOne(mongo_db)
        crud.set_options(CrudOptions(PROJECT_ID, USER))
        crud.set_collection(collection.CRUD)
        _id = ObjectId()
        await crud.insert_update(
            {PROJECT_ID: _id, NAME: "name", "pe": "pa", "y": "agua", "pa": "la", "seca": 1}
        )

        crud.options.set_projection({NAME: 0, "pe": 1, "pa": 0, "y": 1})

        with pytest.raises(ValueError) as excinfo:
            await crud.get()

        assert "You cannot currently mix" in str(excinfo)


class TestCrudGetWithLimit:
    crud: CrudOne = CrudOne(mongo_db)
    crud.set_collection(collection.CRUD)

    async def test_get_with_limit(self) -> None:
        ID1: ObjectId = ObjectId()
        createdData1: TData = await insert_one_by_id(str(ID1), self.crud)
        ID2: ObjectId = ObjectId()
        await insert_one_by_id(str(ID2), self.crud)

        _filter: Dict = {"one": 1}
        retrievedData: List[TData] = await self.crud.get_with_limit(**_filter)

        assert len(retrievedData) == 1
        assert_createdData_equals_retievedData(createdData1, retrievedData[0])

    async def test_get_with_limit_explicit_limit(self) -> None:
        ID1: ObjectId = ObjectId()
        createdData1: TData = await insert_one_by_id(str(ID1), self.crud)
        ID2: ObjectId = ObjectId()
        await insert_one_by_id(str(ID2), self.crud)

        _filter: Dict = {"one": 1}
        limit: int = 1
        retrievedData: List[TData] = await self.crud.get_with_limit(limit, **_filter)

        assert len(retrievedData) == limit
        assert_createdData_equals_retievedData(createdData1, retrievedData[0])

    async def test_get_with_limit_explicit_limit_to_zero(self) -> None:
        ID1: ObjectId = ObjectId()
        await insert_one_by_id(str(ID1), self.crud)
        ID2: ObjectId = ObjectId()
        await insert_one_by_id(str(ID2), self.crud)

        _filter: Dict = {"one": 1}
        limit: int = 0

        with pytest.raises(err.ErrorBase) as excinfo:
            await self.crud.get_with_limit(limit, **_filter)

        assert tr.translate("ERROR_LIMIT_TOO_LOW").format(limit) == str(excinfo.value)

    async def test_get_with_limit_explicit_limit_higher_than_data(self) -> None:
        ID1: ObjectId = ObjectId()
        await insert_one_by_id(str(ID1), self.crud, **{"two": 2})  # type: ignore
        ID2: ObjectId = ObjectId()
        await insert_one_by_id(str(ID2), self.crud, **{"two": 2})  # type: ignore

        _filter: Dict = {"two": 2}
        limit: int = 10
        returnedData: List[TData] = await self.crud.get_with_limit(limit, **_filter)

        assert len(returnedData) == 2

    async def test_get_with_limit_sorting_DESCENDENT(self) -> None:
        random_n: float = random.gauss(5000, 5000)
        ID1: ObjectId = ObjectId()
        await insert_one_by_id(str(ID1), self.crud, **{"two": random_n})  # type: ignore
        ID2: ObjectId = ObjectId()
        await insert_one_by_id(str(ID2), self.crud, **{"two": random_n})  # type: ignore

        returnedData: List[TData] = await self.crud.get_with_limit(1, sort=[], **{"two": random_n})
        assert returnedData[0]["_id"] == ID2 or ID1
        assert len(returnedData) == 1

    async def test_get_with_limit_sorting_ASCENDENT(self) -> None:
        ID1: ObjectId = ObjectId()
        random_n: float = random.gauss(5000, 5000)
        await self.insert_two_entries_with_random_values(ID1, random_n)

        returnedData: List[TData] = await self.crud.get_with_limit(
            1, sort=[(CREATE_DATE, ASCENDING)], **{"two": random_n}
        )

        assert returnedData[0]["_id"] == ID1

    async def insert_two_entries_with_random_values(self, ID1: str, random_n: float) -> None:
        await insert_one_by_id(str(ID1), self.crud, **{"two": random_n})  # type: ignore
        await insert_one_by_id(str(ObjectId()), self.crud, **{"two": random_n})  # type: ignore


class TestCrudGetPagination:
    crud: CrudOne = CrudOne(mongo_db)

    async def test_get_pagination_default_values(self) -> None:
        random_n: float = random.gauss(5000, 5000)
        self.crud.set_collection(f"{collection.CRUD_PAGINATION}_{random_n}")
        await self.insert_n_entries(*[ObjectId(), ObjectId(), ObjectId(), ObjectId()])

        returned_data = await self.crud.get()
        assert len(returned_data) == 4
        self.crud.mongoDB.drop_collection(f"{collection.CRUD_PAGINATION}_{random_n}")

    async def test_get_pagination_default_values_sort_asc(self) -> None:
        random_n: float = random.gauss(5000, 5000)
        self.crud.set_collection(f"{collection.CRUD_PAGINATION}_{random_n}")
        await self.insert_n_entries(*[ObjectId(), ObjectId(), ObjectId(), ObjectId()])
        self.crud.options.set_sort([("_id", 1)])
        returned_data = await self.crud.get()
        assert len(returned_data) == 4
        assert returned_data[0]["_id"] < returned_data[3]["_id"]
        self.crud.mongoDB.drop_collection(f"{collection.CRUD_PAGINATION}_{random_n}")

    async def test_get_pagination_default_values_sort_desc(self) -> None:
        random_n: float = random.gauss(5000, 5000)
        self.crud.set_collection(f"{collection.CRUD_PAGINATION}_{random_n}")
        await self.insert_n_entries(*[ObjectId(), ObjectId(), ObjectId(), ObjectId()])
        self.crud.options.set_sort([("_id", -1)])
        returned_data = await self.crud.get()
        assert len(returned_data) == 4
        assert returned_data[3]["_id"] < returned_data[0]["_id"]
        self.crud.mongoDB.drop_collection(f"{collection.CRUD_PAGINATION}_{random_n}")

    # sourcery no-metrics
    async def test_get_pagination_set_limit_no_skip(self) -> None:
        random_n: float = random.gauss(5000, 5000)
        self.crud.set_collection(f"{collection.CRUD_PAGINATION}_{random_n}")

        ID1 = ObjectId()
        ID2 = ObjectId()
        ID3 = ObjectId()
        ID4 = ObjectId()
        await self.insert_n_entries(*[ID1, ID2, ID3, ID4])

        self.crud.options.set_limit(2)
        self.crud.options.set_skip(0)

        returned_data = await self.crud.get()
        assert len(returned_data) == 2
        for elm in returned_data:
            assert elm["_id"] == ID2 or ID3 or ID4

        self.crud.mongoDB.drop_collection(f"{collection.CRUD_PAGINATION}_{random_n}")

    async def test_get_pagination_set_skip_no_limit(self) -> None:
        # sourcery no-metrics
        random_n: float = random.gauss(5000, 5000)
        self.crud.set_collection(f"{collection.CRUD_PAGINATION}_{random_n}")
        ID1 = ObjectId()
        ID2 = ObjectId()
        ID3 = ObjectId()
        ID4 = ObjectId()
        await self.insert_n_entries(*[ID1, ID2, ID3, ID4])

        self.crud.options.set_limit(0)
        self.crud.options.set_skip(1)

        returned_data = await self.crud.get()
        assert len(returned_data) == 3
        for elm in returned_data:
            assert elm["_id"] == ID1 or ID2 or ID3
        self.crud.mongoDB.drop_collection(f"{collection.CRUD_PAGINATION}_{random_n}")

    # sourcery no-metrics
    async def test_get_pagination_set_skip_and_limit(self) -> None:
        random_n: float = random.gauss(5000, 5000)
        self.crud.set_collection(f"{collection.CRUD_PAGINATION}_{random_n}")

        ID1 = ObjectId()
        ID2 = ObjectId()
        ID3 = ObjectId()
        ID4 = ObjectId()
        await self.insert_n_entries(*[ID1, ID2, ID3, ID4])

        self.crud.options.set_skip(1)
        self.crud.options.set_limit(2)

        returned_data = await self.crud.get()
        assert len(returned_data) == 2
        for elm in returned_data:
            assert elm["_id"] == ID2 or ID3

        self.crud.mongoDB.drop_collection(f"{collection.CRUD_PAGINATION}_{random_n}")

    # sourcery no-metrics
    async def test_get_pagination_set_pagination(self) -> None:
        random_n: float = random.gauss(5000, 5000)
        self.crud.set_collection(f"{collection.CRUD_PAGINATION}_{random_n}")
        ID1 = ObjectId()
        ID2 = ObjectId()
        ID3 = ObjectId()
        ID4 = ObjectId()
        await self.insert_n_entries(*[ID1, ID2, ID3, ID4])

        self.crud.options.set_pagination(1, 2)

        returned_data = await self.crud.get()
        assert len(returned_data) == 2
        for elm in returned_data:
            assert elm["_id"] == ID1 or ID2
        self.crud.mongoDB.drop_collection(f"{collection.CRUD_PAGINATION}_{random_n}")

    async def insert_n_entries(self, *ids: List) -> None:
        for id in ids:
            await self.crud.insert_update({"_id": id})


def assert_createdData_equals_retievedData(createdData: TData, retrievedData: TData) -> None:
    for elm in createdData:
        if elm not in OMIT_FIELDS:
            assert createdData[elm] == retrievedData[elm]


async def insert_one_by_id(id: str, crud: CrudOne, **additionalData: Dict[Any, Any]) -> TData:
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
    assert bool(crud.get_messages())
    assert not bool(crud.get_data())
    assert crud.get_messages()[0] == str(excinfo.value)


def assertErrorDelete(crud: CrudOne, excinfo: Any) -> None:
    assert bool(crud.get_messages())
    assert not bool(crud.get_data())
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
    assert CREATE_DATE in crud.get_data()
    assert CREATE_USER in crud.get_data()
    assert MODIFIED_USER not in crud.get_data()
    assert MODIFIED_DATE not in crud.get_data()


def assertUpdate(crud: CrudOne, entry: TData, msg: str) -> None:
    assert bool(crud.get_messages())
    assert bool(crud.get_data())
    assertData(crud.get_data(), entry)
    assertMessage(crud.get_messages(), msg, crud.lang)
    assert CREATE_DATE in crud.get_data()
    assert CREATE_USER in crud.get_data()
    assert MODIFIED_USER in crud.get_data()
    assert MODIFIED_DATE in crud.get_data()


def assertSoftDelete(crud: CrudOne, entry: TData, msg: str) -> None:
    assert bool(crud.get_messages())
    assert bool(crud.get_data())
    assertData(crud.get_data(), entry)
    assertMessage(crud.get_messages(), msg, crud.lang)
    assert CREATE_DATE in crud.get_data()
    assert CREATE_USER in crud.get_data()
    assert DELETED_DATE in crud.get_data()
    assert DELETED_USER in crud.get_data()


def assertData(listSchemas: List[TData], schema: TData) -> None:
    for elm in schema:
        if elm in OMIT_FIELDS:
            continue
        assert schema[elm] == listSchemas[0][elm]


def assertMessage(listMessages: List[str], msg: str, lang: str = "en") -> None:
    assert tr.translate(msg, lang)[:30] in listMessages[0]
