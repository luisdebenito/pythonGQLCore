from typing import Any, Dict, List, TypeVar

from aiodataloader import DataLoader
from bson.objectid import ObjectId

import _python_core.Errors as err

TObject = TypeVar("TObject", bound="DataLoader")


class AriadneDataLoader(DataLoader):
    def __init__(self, context: Any, objMany: Any, *args: Any, **kwargs: Any) -> None:
        self.context = context
        self.objMany = objMany

        super().__init__(*args, **kwargs)

    @classmethod
    def for_context(cls: TObject, context: Any, objMany: Any) -> Any:
        # take collection as it is unique
        if not (key := objMany.collection):
            raise err.ErrorBase(f"Data loader {cls} does not define a context key")

        loaders = context.setdefault("loaders", {})

        if key not in loaders:
            loaders[key] = cls(context=context, objMany=objMany)

        loader = loaders[key]
        if not isinstance(loader, cls):
            raise err.ErrorBase(f"Data loader {cls} does not define a context key")

        return loader

    async def batch_load_fn(self, ids: List[str]) -> List[Dict | None]:
        query = {"$or": [{"_id": ObjectId(id)} for id in ids]}
        data = await self.objMany.get_all(**query)

        result: List[Dict | None] = [None] * len(ids)
        for index, _id in enumerate(ids):
            for obj in data:
                if str(obj.get("_id")) == _id:
                    result[index] = obj

        return result
