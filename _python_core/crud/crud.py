import copy
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, TypeVar, Union

from bson import ObjectId
from pymongo import DESCENDING, MongoClient
from pymongo.database import Database

from _python_core import Errors as err
from _python_core.crud.crud_constants import (
    ACTIVE,
    CREATE_DATE,
    CREATE_USER,
    DELETED_USER,
    MAXDATE,
    MINDATE,
    NAME,
    REQUESTDATE,
)
from _python_core.crud.crud_options import CrudOptions
from _python_core.http_codes import HTTPCode
from _python_core.translations import Translations as tr

TData = Dict[str, Any]  # Type object as defined in GQL Schema
TMessages = List[str]
TInsertedData = List[TData]

TCrud = TypeVar("TCrud", bound="Crud")


class ErrorCRUD(err.ErrorBase):
    def __init__(self, msg: str) -> None:
        self.message: str = msg
        super().__init__(self.message)


class Crud(ABC):
    default_sort: List[Tuple] = [(CREATE_DATE, DESCENDING)]

    def __init__(self, mongoDB: Database, lang: str = "en") -> None:
        self.mongoDB: Database = mongoDB
        self.options: CrudOptions = CrudOptions(lang=lang)
        self.mongo: MongoClient = None
        self.collection: str = ""
        self.lang = lang

        self.http_code: HTTPCode = None

    @abstractmethod
    def set_options(self, options: CrudOptions) -> None:
        pass  # pragma: no cover

    def _verifyLanguage(self) -> None:
        if self.options.lang != self.lang:
            raise ErrorCRUD(tr.translate("ERROR_CRUDOPTIONS_LANGUAGE_DISCREPANCY", self.lang))

    @abstractmethod
    def set_collection(self, collection: str) -> None:
        pass

    @abstractmethod
    def set_language(self, lang: str) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def translate(self, msg: str) -> str:
        pass

    async def get(self, sort: List[Tuple] = [], **filter: Dict) -> List[TData]:
        sort = self._update_sort(self.options.sort)
        self.set_default_filters(filter)
        return list(
            self.mongo.find(filter, self.options.projection)
            .sort(sort)
            .skip(self.options.skip)
            .limit(self.options.limit)
        )

    async def get_single(self, sort: List[Tuple] = [], **filter: Any) -> TData:
        sort = self._update_sort(sort)
        self.set_default_filters(filter)
        result: List[TData] = list(self.mongo.find(filter, self.options.projection).sort(sort))
        return result[0] if result else {}

    async def get_with_limit(
        self, limit: int = 1, sort: List[Tuple] = [], **filter: Any
    ) -> List[TData]:

        if limit <= 0:
            raise ErrorCRUD(self.translate("ERROR_LIMIT_TOO_LOW").format(limit))

        sort = self._update_sort(sort)
        self.set_default_filters(filter)
        return list(self.mongo.find(filter, self.options.projection).sort(sort).limit(limit))

    def _update_sort(self, sort: List[Tuple]) -> List[Tuple]:
        default_sort = self._tweak_default_entry(sort)
        sort.extend(default_sort)
        return sort

    def _tweak_default_entry(self, sort: List[Tuple]) -> List[Tuple]:
        default_sort: List[Tuple] = copy.deepcopy(self.default_sort)
        for item in sort:
            if item[0] == CREATE_DATE:
                default_sort = []
        return default_sort

    async def get_by_id(self, id: Union[str, ObjectId]) -> TData:
        if self._is_id_a_valid_objectId(id):
            return self.mongo.find_one({"_id": ObjectId(id)})

        return {}

    def _is_id_a_valid_objectId(self, id: Union[str, ObjectId]) -> bool:
        return ObjectId.is_valid(str(id))

    def set_default_filters(self, filter: Dict) -> None:
        if self.options._is_skip_deleted_entries_enable():
            filter[DELETED_USER] = {"$exists": False}
        filter |= self.options.additionalFilter

        if len(self.options.idsFilter):
            filter["_id"] = {"$in": self._set_ids_filter()}

        if self.options._is_skip_inactive_entries_enable():
            filter[ACTIVE] = {"$in": [None, True]}

        if self.options._is_date_filter_enabled():
            self._tweak_filter_date(filter)

        if self.options._is_user_filter_enabled():
            filter[CREATE_USER] = {"id": self.options.userId}

    def _set_ids_filter(self) -> List[str] | None:
        newIdsObject: List[str] = []
        for id in self.options.idsFilter:
            if not self._is_id_a_valid_objectId(id):
                raise err.ErrorBase(tr.translate("ERROR_ID_FIELD"))
            newIdsObject.append(ObjectId(id))
        return newIdsObject

    def _tweak_filter_date(self, filter: Dict) -> None:
        dateFilters = self.options.dateFilter
        if dateFilters.get(REQUESTDATE):
            self._tweak_filter_for_request_date(filter, dateFilters)

        elif dateFilters.get(MINDATE) and dateFilters.get(MAXDATE):
            self._tweak_filter_for_date_range(filter, dateFilters)

        elif dateFilters.get(MINDATE):
            self._tweak_filter_for_min_date(filter, dateFilters)

        elif dateFilters.get(MAXDATE):
            self._tweak_filter_for_max_date(filter, dateFilters)

    def _tweak_filter_for_max_date(self, filter: Dict, dateFilters: Dict) -> None:
        endDate = dateFilters[MAXDATE].replace(hour=23, minute=59, second=59)
        filter[dateFilters[NAME]] = {"$lte": endDate}

    def _tweak_filter_for_min_date(self, filter: Dict, dateFilters: Dict) -> None:
        startDate = dateFilters[MINDATE].replace(hour=0, minute=0, second=0)
        filter[dateFilters[NAME]] = {"$gte": startDate}

    def _tweak_filter_for_date_range(self, filter: Dict, dateFilters: Dict) -> None:
        startDate = dateFilters[MINDATE].replace(hour=0, minute=0, second=0)
        endDate = dateFilters[MAXDATE].replace(hour=23, minute=59, second=59)
        filter[dateFilters[NAME]] = {"$gte": startDate, "$lte": endDate}

    def _tweak_filter_for_request_date(self, filter: Dict, dateFilters: Dict) -> None:
        startDate = dateFilters[REQUESTDATE].replace(hour=0, minute=0, second=0)
        endDate = dateFilters[REQUESTDATE].replace(hour=23, minute=59, second=59)
        filter[dateFilters[NAME]] = {"$gte": startDate, "$lte": endDate}
