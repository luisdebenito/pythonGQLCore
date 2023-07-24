import os
import sys
from typing import Any, Dict

import pytest

if os.getenv("MOCK_TEST") == "True":
    from mongomock import Database, Collection
else:
    from pymongo.database import Database
    from pymongo.collection import Collection

from conftest import mongo_db

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))
from _python_core.crud.crud_constants import OMIT_FIELDS
from _python_core.crud.crud_single import CrudOne
from _python_core.crud.crud_options import CrudOptions
from _python_core.translations import Translations as tr
import _python_core.Errors as err

TData = Dict[str, Any]  # Type object as defined in GQL Schema

# Kurt USERID
USER = "02477c69-56f4-4e77-921a-23a2a82a335e"
PROJECT_ID = "12070c789f30472094bbcf61923ecab4"


class collection:
    CRUD = "crud"
    CHANGELOG = "changeLog"


class TestCRUD_createOne_withOptions:
    crud: CrudOne = CrudOne(mongo_db)

    def test_createCRUD(self) -> None:
        assertCreateCRUDObject(self.crud)

    def test_createCRUD_with_options(self) -> None:
        self.crud.set_options(CrudOptions(PROJECT_ID, USER))
        assertCreateCrudOptions(self.crud.options)

    def test_createCRUD_with_options_spanish_Error(self) -> None:
        lang: str = "es"
        crudSpanish: CrudOne = CrudOne(mongo_db, lang=lang)
        with pytest.raises(err.ErrorBase) as excinfo:
            crudSpanish.set_options(CrudOptions(PROJECT_ID, USER))
        assert tr.translate("ERROR_CRUDOPTIONS_LANGUAGE_DISCREPANCY", lang) == str(excinfo.value)

    def test_createCRUD_with_options_spanish(self) -> None:
        lang: str = "es"
        crudSpanish: CrudOne = CrudOne(mongo_db, lang=lang)
        crudSpanish.set_options(CrudOptions(PROJECT_ID, USER, lang=lang))
        assert crudSpanish.lang == crudSpanish.options.lang

    def test_setCollection(self) -> None:
        self.crud.set_collection(collection.CRUD)
        assert isinstance(self.crud.mongo, Collection)
        assert self.crud.collection == collection.CRUD


def assertCreateCRUDObject(crud: CrudOne) -> None:
    assert isinstance(crud.mongoDB, Database)
    assert isinstance(crud.message, str)
    assert isinstance(crud.data, Dict)


def assertCreateCrudOptions(optCrud: CrudOptions) -> None:
    assert optCrud.projectId == PROJECT_ID
    assert optCrud.userId == USER
    assert optCrud.actionChangeLog == "Update"
    assert optCrud.omitFields == OMIT_FIELDS
    assert optCrud.updateAuditFields is True
    assert optCrud.updateChangeLog is True
    assert optCrud.softDelete is True
    assert optCrud.filterByUser is False
