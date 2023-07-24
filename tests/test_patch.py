import os
import sys
from mongomock import ObjectId

import pytest
from conftest import mongo_db

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.crud.crud_single import CrudOne


class collection:
    CRUD = "crud"
    CHANGELOG = "changeLog"


class TestChangelog:
    crud = CrudOne(mongo_db)
    crud.set_collection(collection.CRUD)

    async def test_get_changelog_for_project(self) -> None:
        ID = ObjectId()
        original_data = {"_id": ID, "one": 1}
        await self.crud.insert_update(original_data)

        edited_data = {"_id": ID, "one": 2}
        await self.crud.insert_update(edited_data)
        result = self.crud.get_data()

        assert result["one"] == 2
