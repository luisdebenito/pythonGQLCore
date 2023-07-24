from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database

from _python_core.get_differences import GetDifferences

UPDATE = "Update"
OMIT_FIELDS: List[str] = [
    "_id",
    "id",
    "createUser",
    "createDate",
    "modifiedDate",
    "modifiedUser",
    "deletedUser",
    "deletedDate",
]

THistory = Dict[str, Dict[str, str]]
TData = Dict[str, Any]


class History:
    collection: str = "changeLog"

    def __init__(self, schema: TData):
        self.changeLog: List[THistory] = []
        self.entry: TData = schema
        self.parentID: Optional[str] = self._get_parent_id()
        self.lang = "en"
        self.action = UPDATE
        self.history: Dict = {
            "parentID": self.parentID,
            "changeLog": [],
            "collection": "",
            "action": self.action,
            "projectId": "",
        }
        self.omitFields: List[str] = OMIT_FIELDS

    def set_collection(self, collection: str) -> None:
        self.history["collection"] = collection

    def set_action(self, action: str) -> None:
        self.action = action
        self.history["action"] = action

    def get(self) -> TData:
        return self.history

    async def calculate(self, mongoDB: Database) -> None:
        self.mongo: Collection = mongoDB[self.history["collection"]]
        await self._set_history_for_update()

    async def _set_history_for_update(self) -> None:
        if self._is_update_entry():
            self.history["changeLog"] = await self._get_history()

    def _is_update_entry(self) -> bool:
        return self.action == UPDATE

    async def _get_history(self) -> List[THistory]:
        old_entry: Optional[TData] = self.mongo.find_one({"_id": ObjectId(self.parentID)})
        diffs: GetDifferences = GetDifferences(self.lang, *self.omitFields)
        diffs.calculate(self.entry, old_entry)
        return diffs.get_differences()

    def _get_parent_id(self) -> str:
        return str(self.entry.get("_id"))
