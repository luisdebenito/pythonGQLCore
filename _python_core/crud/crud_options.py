from datetime import datetime
import json
from typing import Dict, List, Tuple
from _python_core.constants import DATETIME, EXTRA_INFO

from _python_core.crud.crud_constants import (
    CREATE,
    CREATE_DATE,
    DELETE,
    MAXDATE,
    MINDATE,
    NAME,
    OMIT_FIELDS,
    REQUESTDATE,
    UPDATE,
)
from _python_core.functions import transform_list_dict_to_list_tuple
from _python_core.Errors import ErrorBase
from _python_core.translations import Translations as tr

DEFAULT_LIMIT = 0
DEFAULT_SKIP = 0


class CrudOptions:
    def __init__(self, projectId: str = "", userId: str = "", lang: str = "en") -> None:
        self.projectId: str = projectId
        self.userId: str = userId
        self.lang: str = lang

        self.omitFields: List[str] = OMIT_FIELDS
        self.updateAuditFields: bool = True
        self.updateChangeLog: bool = True
        self.actionChangeLog: str = UPDATE
        self.softDelete: bool = True
        self.skipDeletedEntries: bool = True
        self.skipInactiveEntries: bool = True
        self.filterByUser: bool = False
        self.sort: List[Tuple] = []
        self.projection: Dict | None = None

        self.dateFilter: Dict = {
            NAME: CREATE_DATE,
            MINDATE: None,
            MAXDATE: None,
            REQUESTDATE: None,
        }

        self.limit: int = DEFAULT_LIMIT
        self.skip: int = DEFAULT_SKIP

        self.additionalFilter: Dict = {}
        self.extraInfo: Dict = {}
        self.idsFilter: List = []

    def set_language(self, lang: str) -> None:
        self.lang = lang

    def set_omitFields(self, omitFields: List[str]) -> None:
        self.omitFields = omitFields

    def set_updateAuditFields(self, updateAuditFields: bool) -> None:
        self.updateAuditFields = updateAuditFields

    def set_updateChangeLog(self, updateChangeLog: bool) -> None:
        self.updateChangeLog = updateChangeLog

    def set_actionChangeLog(self, actionChangeLog: str) -> None:
        self.actionChangeLog = actionChangeLog
        self._check_valid_actionChangeLog()

    def set_softDelete(self, softDelete: bool) -> None:
        self.softDelete = softDelete

    def set_skipDeletedEntries(self, skipDeletedEntries: bool) -> None:
        self.skipDeletedEntries = skipDeletedEntries

    def set_skipInactiveEntries(self, skipInactiveEntries: bool) -> None:
        self.skipInactiveEntries = skipInactiveEntries

    def set_filterByUser(self, filterByUser: bool) -> None:
        self.filterByUser = filterByUser

    def set_dateFilter(self, dateFilter: Dict) -> None:
        if name := dateFilter.get(NAME):
            self.dateFilter[NAME] = name
        for key in [MAXDATE, MINDATE, REQUESTDATE]:
            if value := dateFilter.get(key):
                self.dateFilter[key] = (
                    datetime.strptime(value, DATETIME) if isinstance(value, str) else value
                )

    def set_limit(self, limit: int) -> None:
        self.limit = limit

    def set_skip(self, skip: int) -> None:
        self.skip = skip

    def set_pagination(self, page: int = 0, limit: int = DEFAULT_LIMIT) -> None:
        self.skip = page * limit
        self.limit = limit

    def set_projection(self, projection: Dict | None = None) -> None:
        self.projection = projection

    def set_sort(self, sort: List[Tuple]) -> None:
        self.sort = sort

    def set_optionsFromGQL(
        self,
        softDelete: bool = True,
        updateAuditFields: bool = True,
        updateChangeLog: bool = True,
        skipDeletedEntries: bool = True,
        skipInactiveEntries: bool = True,
        idsFilter: List = [],
        dateFilter: Dict = {},
        skip: int = DEFAULT_SKIP,
        limit: int = DEFAULT_LIMIT,
        page: int = None,
        filterByUser: bool = False,
        sort: str = "[]",
        projection: Dict | None = None,
        **kwargs: Dict,
    ) -> None:
        self.updateAuditFields = updateAuditFields
        self.updateChangeLog = updateChangeLog
        self.softDelete = softDelete
        self.skipDeletedEntries = skipDeletedEntries
        self.skipInactiveEntries = skipInactiveEntries
        self.set_dateFilter(dateFilter)
        self.limit = limit
        self.skip = page * limit if page else skip
        self.filterByUser = filterByUser
        self.idsFilter = idsFilter
        self.sort = transform_list_dict_to_list_tuple(json.loads(sort))
        self.projection = projection
        # Not possible send id or date in additionalFilter. Use idsfilter or datefilter instead
        self.additionalFilter = json.loads(kwargs.get("additional_filter", "{}")) if kwargs else {}  # type: ignore
        self.extraInfo = kwargs.get(EXTRA_INFO, {})

    def _check_valid_actionChangeLog(self) -> None:
        if self.actionChangeLog not in [CREATE, UPDATE, DELETE]:
            raise ErrorBase(tr.translate("ERROR_WRONG_ACTION_CHANGELOG", self.lang))

    def _is_valid_date_filter(self, dateFilter: Dict) -> bool:
        return bool(dateFilter.get(NAME)) and any(
            [
                dateFilter.get(MINDATE),
                dateFilter.get(MAXDATE),
                dateFilter.get(REQUESTDATE),
            ]
        )

    def _is_date_filter_enabled(self) -> bool:
        return self._is_valid_date_filter(self.dateFilter)

    def _is_skip_deleted_entries_enable(self) -> bool:
        return self.skipDeletedEntries

    def _is_skip_inactive_entries_enable(self) -> bool:
        return self.skipInactiveEntries

    def _is_user_filter_enabled(self) -> bool:
        return self.filterByUser
