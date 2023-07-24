import os
import sys
from typing import Any, Dict, List, TypeVar, Union

from bson.objectid import ObjectId

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core import BaseClass as nbc

TData = Dict[str, Any]
TMockManyObjects = TypeVar("TMockManyObjects", bound="MockManyObjects")
TMockSingleObject = TypeVar("TMockSingleObject", bound="MockSingleObject")


class MockBase:
    lang: str = "en"
    collection: str = "MOCK"


class MockManyObjects(MockBase, nbc.BaseMany):
    def __init__(self, **kwargs: Any) -> None:
        nbc.BaseMany.__init__(self, **kwargs)
        self._initialize_values()

    def set_schemas(self, entries: List[TData]) -> None:
        self.schemas: List[TData] = entries
        self._set_mocks_from_schemas()
        self._set_ids_froms_schemas()

    def _set_mocks_from_schemas(self) -> None:
        self.mocks = [MockSingleObject() for _ in self.schemas]
        for idx, mock in enumerate(self.mocks):
            mock.set_schema(self.schemas[idx])

    def _set_ids_froms_schemas(self) -> None:
        for schema in self.schemas:
            if bool(schema.get("id")):
                self.ids.append(str(schema.get("id")))
            elif bool(schema.get("_id")):
                self.ids.append(str(schema.get("_id")))

    def set_schemas_from_ids(self, ids: List[str]) -> None:
        mocks: List[TData] = [{"id": id} for id in ids]
        self.set_schemas(mocks)

    async def validate_to_insertUpdate(self) -> None:
        self.validSchemas = self.schemas

    async def validate_to_delete(self) -> None:
        self.validSchemas = self.schemas

    def _initialize_values(self) -> None:
        self.errors: List = []
        self.validSchemas = []
        self.schemas = []
        self.inValidSchemas: List[TData] = []
        self.ids: List[str] = []


class MockSingleObject(MockBase, nbc.BaseOne):
    def __init__(self, **kwargs: Any) -> None:
        nbc.BaseOne.__init__(self, **kwargs)
        self._initialize_values()

    async def validate_to_insertUpdate(self) -> None:
        return

    async def validate_to_delete(self) -> None:
        return

    def _initialize_values(self) -> None:
        self.error: Union[str, Dict[str, str]] = {}
        self.schema: TData = {}

    def set_schema(self, entry: TData) -> None:
        self.schema = entry

    def set_schema_from_id(self, id: Union[str, ObjectId]) -> None:
        self.schema = {"_id": ObjectId(str(id))}
