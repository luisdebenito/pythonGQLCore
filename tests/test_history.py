import os
import sys
from typing import Any, Dict

import pytest
from bson import ObjectId

from conftest import mongo_db

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.history import History
from _python_core.crud.crud_single import CrudOne

TData = Dict[str, Any]  # Type object as defined in GQL Schema

# Kurt USERID
USER = "02477c69-56f4-4e77-921a-23a2a82a335e"
PROJECT_ID = "12070c789f30472094bbcf61923ecab4"


class collection:
    CRUD = "crud"
    CHANGELOG = "changeLog"


class TestChangelogCreate:
    async def test_create(self, id: ObjectId = ObjectId()) -> None:
        entry: TData = {"_id": id, "one": 1}
        history: History = History(entry)
        history.set_collection(collection.CRUD)
        history.set_action("Create")
        await history.calculate(mongo_db)

        assert history.history["action"] == "Create"
        assert history.history["parentID"] == str(id)
        assert history.history["collection"] == "crud"
        assert history.history["projectId"] == ""
        assert history.history["changeLog"] == []


class TestChangelogUpdate:
    crud: CrudOne = CrudOne(mongo_db)
    crud.set_collection(collection.CRUD)

    async def test_update(self) -> None:
        ID = ObjectId()
        entry: TData = {"_id": ID, "one": 1}
        await self.crud.insert_update(entry)

        entry["one"] = 2
        history: History = History(entry)
        history.set_collection(collection.CRUD)
        await history.calculate(mongo_db)

        assert history.history["action"] == "Update"
        assert history.history["parentID"] == str(ID)
        assert history.history["collection"] == "crud"
        assert history.history["projectId"] == ""
        assert history.history["changeLog"] == [{"field": "one", "oldValue": "1", "newValue": "2"}]


class TestChangelogDelete:
    crud: CrudOne = CrudOne(mongo_db)
    crud.set_collection(collection.CRUD)

    async def test_delete(self) -> None:
        entry: TData = {"one": 1}
        history: History = History(entry)
        history.set_collection(collection.CRUD)
        history.set_action("Delete")
        await history.calculate(mongo_db)

        assert history.history["action"] == "Delete"
