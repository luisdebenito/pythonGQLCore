import os
import sys
from typing import Any, Dict, List

from conftest import mongo_db

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.crud.crud_many import CrudMany
from _python_core.crud.crud_options import CrudOptions
from _python_core.changelog import Changelog

TData = Dict[str, Any]  # Type object as defined in GQL Schema

# Kurt USERID
USER = "02477c69-56f4-4e77-921a-23a2a82a335e"
PROJECT_ID = "12070c789f30472094bbcf61923ecab4"


class collection:
    CRUD = "crud"
    CHANGELOG = "changeLog"


class TestChangelog:
    changelog: Changelog = Changelog()
    changelog.set_crud(mongo_db)
    changelog.set_crud_options(CrudOptions(PROJECT_ID, USER))

    crud: CrudMany = CrudMany(mongo_db)
    crud.set_collection(collection.CHANGELOG)
    crud.set_options(CrudOptions(PROJECT_ID, USER))
    crud.options.set_updateChangeLog(False)

    async def test_get_changelog_for_project(self) -> None:
        inputs: List = [
            {
                "id": "624da8bd25085bf60c9df1d6",
                "parentID": "624da8bd25085bf60c9df1d4",
                "changeLog": [],
                "collection": "crud",
                "action": "Create",
                "projectId": "",
            }
        ]
        await self.crud.insert_update(inputs)

        results = await self.changelog.get_by_project()

        for elm in results:
            assert elm["project"]["id"] == PROJECT_ID

    async def test_get_changelog_for_parentId(self) -> None:
        inputs: List = [
            {
                "id": "624da8bd25085bf60c9df1d6",
                "parentID": "624da8bd25085bf60c9df1d4",
                "changeLog": [],
                "collection": "crud",
                "action": "Create",
                "projectId": "",
            },
            {
                "id": "624da8bd25095bf60c9df1d6",
                "parentID": "624da8bf1d4",
                "changeLog": [],
                "collection": "crud",
                "action": "Create",
                "projectId": "",
            },
        ]
        await self.crud.insert_update(inputs)

        results = await self.changelog.get_by_project_and_diaryId("624da8bd25085bf60c9df1d4")

        for elm in results:
            assert elm["parentID"] == "624da8bd25085bf60c9df1d4"
