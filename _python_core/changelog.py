from typing import Any, Dict, List

from _python_core.BaseClass import BaseOne

PROJECT = "project"
PARENTID = "parentID"

TChangelog = Dict[str, Any]


class Changelog(BaseOne):
    collection: str = "changeLog"

    async def get_by_project(self) -> List[Dict]:
        _filter: Dict[str, Any] = {
            PROJECT: {"id": self.handlerCrudSingle.options.projectId},
        }
        return await self.get_all(**_filter)

    async def get_by_project_and_diaryId(self, diaryId: str) -> None:
        _filter: Dict[str, Any] = {
            PROJECT: {"id": self.handlerCrudSingle.options.projectId},
            PARENTID: diaryId,
        }
        return await self.get_all(**_filter)

    async def validate_to_insertUpdate(self) -> None:
        ...

    async def validate_to_delete(self) -> None:
        ...
