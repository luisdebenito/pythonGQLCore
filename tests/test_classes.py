import os
import sys
import copy
from typing import Dict, List, Union

import pytest
from bson import ObjectId

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

import _python_core.Errors as err
from _python_core.http_codes import HTTPCode
from _python_core.crud.crud_many import CrudMany, TData
from _python_core.translations import Translations as tr
from _python_core.crud.crud_options import CrudOptions
from _python_core.crud.crud_constants import (
    CREATE,
    CREATE_DATE,
    CREATE_USER,
    UPDATE,
    MODIFIED_DATE,
    MODIFIED_USER,
    DELETE,
    DELETED_DATE,
    DELETED_USER,
)

import mockClass as mc
from conftest import mongo_db

USER = "02477c69-56f4-4e77-921a-23a2a82a335e"
PROJECT_ID = "12070c789f30472094bbcf61923ecab4"


class collection:
    MOCK = "mock"


class _MockContext:
    def setdefault(self, key: str, content: Dict) -> Dict:
        return {}


class MockInfo:
    context = _MockContext()


class TestClasses_Single:
    single = mc.MockSingleObject()
    single.set_crud(mongo_db)
    single.handlerCrudSingle.set_options(CrudOptions(PROJECT_ID, USER, single.lang))

    def test_SingleObjects_create(self) -> None:
        assert self.single

    def test_set_crud_with_crudOptions(self) -> None:
        test_crud = mc.MockSingleObject(lang="de")
        crudOptions = CrudOptions("MY_PROJECT", "MY_USER")
        test_crud.set_crud(mongo_db, crudOptions)

        assert test_crud.handlerCrudSingle.options.projectId == "MY_PROJECT"
        assert test_crud.handlerCrudSingle.options.userId == "MY_USER"

    def test_language(self) -> None:
        test = mc.MockSingleObject(lang="de")
        assert test.lang == "de"

    async def test_SingleObjects_insertUpdate(self, ID1: ObjectId = ObjectId()) -> None:
        entry = {"_id": ID1, "code": 1}
        self.single.set_schema(entry)
        await self.single.insert_update()

        assert tr.translate("MSG_SUCCESSFULLY_INSERTED")[:-2] in self.single.get_message()
        assert self.single.get_http_code() == HTTPCode.CODE_200
        assert self.single.get_data()["code"] == 1

    async def test_SingleObjects_delete(self) -> None:
        data_id = ObjectId()
        entry = {"_id": data_id, "code": 1}
        self.single.set_schema(entry)
        await self.single.insert_update()
        await self.single.delete()

        assert tr.translate("MSG_SUCCESSFULLY_SOFT_DELETED")[:-2] in self.single.get_message()

    async def test_SingleObjects_get_all(self) -> None:
        data_id = ObjectId()
        entry = {"_id": data_id, "code": 1}
        self.single.set_schema(entry)
        await self.single.insert_update()

        data = await self.single.get_all(**{"_id": data_id})
        assert len(data) == 1

    async def test_SingleObjects_get_by_id(self) -> None:
        data_id = ObjectId()
        entry = {"_id": data_id, "code": 1}
        self.single.set_schema(entry)
        await self.single.insert_update()

        data = await self.single.get_by_id(data_id)
        assert data["code"] == 1

    async def test_SingleObjects_get_with_limit(self) -> None:
        data_id = ObjectId()
        entry = {"_id": data_id, "code": 1}
        self.single.set_schema(entry)
        await self.single.insert_update()

        data = await self.single.get_with_limit(limit=1, **{"_id": data_id})
        assert len(data) == 1

    async def test_SingleObjects_get_single(self) -> None:
        data_id = ObjectId()
        entry = {"_id": data_id, "code": 1}
        self.single.set_schema(entry)
        await self.single.insert_update()

        data = await self.single.get_single(**{"_id": data_id})

        assert data["_id"] == data_id

    async def test_SingleObjects_get_error_str(self) -> None:
        self.single.error = "Error"
        assert self.single.get_error() == "Error"

    async def test_SingleObjects_get_error_dict(self) -> None:
        self.single.error = {"Error": "one"}
        assert self.single.get_error() == {"Error": "one"}

    async def test_SingleObjects_reference_resolver(self) -> None:
        data_id = ObjectId()
        await self.test_SingleObjects_insertUpdate(data_id)

        data = await self.single.reference_resolver(MockInfo)

        assert data["code"] == 1

    async def test_SingleObjects_delete_hard(self) -> None:
        data_id = ObjectId()
        await self.test_SingleObjects_insertUpdate(data_id)
        await self.single.delete()

        assert tr.translate("MSG_SUCCESSFULLY_SOFT_DELETED")[:-2] in self.single.get_message()

    async def test_SingleObjects_not_empty_data(self) -> None:
        _id = ObjectId()
        await self.test_SingleObjects_insertUpdate(_id)
        assert self.single._is_empty() is False

    async def test_SingleObjects_empty_data(self) -> None:
        self.single.set_schema({})

        with pytest.raises(err.ErrorEmptyData) as excinfo:
            self.single._is_empty()

        assert tr.translate("ERROR_EMPTY_DATA") in str(excinfo.value)

    async def test_SingleObjects_getID_from_entry(self) -> None:
        ID = ObjectId()
        self.single.set_schema_from_id(ID)
        assert self.single._getIDFromEntry() == str(ID)

    async def test_SingleObjects_getID_from_entry_raises(self) -> None:
        self.single.set_schema({})
        with pytest.raises(err.ErrorInvalidID) as excinfo:
            self.single._getIDFromEntry()

        assert tr.translate("ERROR_MISSING_ID") in str(excinfo.value)

    async def test_SingleObjects_getID_from_entry_no_raises(self) -> None:
        self.single.set_schema({})
        data_id: Union[str, None] = self.single._getIDFromEntry(raiseException=False)
        assert data_id is None

    async def test_SingleObjects_reset_errors(self) -> None:
        self.single.set_schema({})
        self.single.error = "Error"
        self.single.reset_errors()
        assert self.single.error == {}

    async def test_SingleObjects_test_bulk_upload(self) -> None:
        self.single.set_bulk_upload(True)
        assert self.single.bulkUpload is True
        self.single.set_bulk_upload(False)

    async def test_SingleObjects_test_set_options(self) -> None:
        crudOptions: CrudOptions = CrudOptions("PROJECT", "USER")
        oldCrudOptions: CrudOptions = copy.deepcopy(self.single.handlerCrudSingle.options)
        self.single.set_crud_options(crudOptions)
        assert self.single.handlerCrudSingle.options.projectId == "PROJECT"
        assert self.single.handlerCrudSingle.options.userId == "USER"
        self.single.set_crud_options(oldCrudOptions)

    async def test_SingleObjects_changeLanguage(self) -> None:
        self.single.set_language("fr")

        assert self.single.lang == "fr"

    async def test_SingleObjects_translate(self) -> None:
        self.single.set_language("en")
        entry = {"code": 1}
        self.single.set_schema(entry)
        self.single.translate("MSG_SUCCESSFULLY_INSERTED")

        assert self.single.translate("MSG_SUCCESSFULLY_INSERTED") == tr.translate(
            "MSG_SUCCESSFULLY_INSERTED"
        ).format(entry)

    def test_validator_created(self) -> None:
        assert self.single.validator.crud == self.single.handlerCrudSingle


class TestClasses_Many:
    many = mc.MockManyObjects()
    many.set_crud(mongo_db)
    many.handlerCrudMany.set_options(CrudOptions(PROJECT_ID, USER, many.lang))

    def test_ManyObjects_create(self) -> None:
        assert self.many

    def test_language(self) -> None:
        test = mc.MockManyObjects(lang="de")
        assert test.lang == "de"

    def test_set_crud_with_crudOptions(self) -> None:
        test_crud = mc.MockManyObjects(lang="de")
        crudOptions = CrudOptions("MY_PROJECT", "MY_USER")
        test_crud.set_crud(mongo_db, crudOptions)

        assert test_crud.handlerCrudMany.options.projectId == "MY_PROJECT"
        assert test_crud.handlerCrudMany.options.userId == "MY_USER"

    async def test_ManyObjects_insertUpdate(self, ID1: ObjectId = ObjectId()) -> None:
        entries = [{"_id": ID1, "code": 1}]
        self.many.set_schemas(entries)
        await self.many.insert_update()

        assertUpdateMany(
            self.many.handlerCrudMany,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200],
            ["MSG_SUCCESSFULLY_INSERTED"],
            [[CREATE]],
        )

    async def test_ManyObjects_insert_empty_schemas(self, ID1: ObjectId = ObjectId()) -> None:
        entries: List[Dict] = []
        self.many.set_schemas(entries)
        await self.many.insert_update()

        assert tr.translate("ERROR_EMPTY_DATA")[:-2] in self.many.get_errors()[0]
        result = self.many.return_mutation()
        assert result.code == 400

    async def test_ManyObjects_soft_delete(self) -> None:
        data_id = ObjectId()
        self.many._initialize_values()
        await self.test_ManyObjects_insertUpdate(data_id)
        await self.many.delete()

        assertUpdateMany(
            self.many.handlerCrudMany,
            HTTPCode.CODE_200,
            [HTTPCode.CODE_200],
            ["MSG_SUCCESSFULLY_SOFT_DELETED"],
            [[CREATE, DELETE]],
        )

    async def test_ManyObjects_hard_delete(self) -> None:
        data_id = ObjectId()
        self.many._initialize_values()
        await self.test_ManyObjects_insertUpdate(data_id)
        self.many.handlerCrudMany.set_softDelete(False)
        await self.many.delete()

        tr.translate("MSG_SUCCESSFULLY_HARD_DELETED")[
            :-2
        ] == self.many.handlerCrudMany.get_messages()

    async def test_ManyObjects_get_all(self) -> None:
        data_id = ObjectId()
        await self.test_ManyObjects_insertUpdate(data_id)
        data = await self.many.get_all(**{"_id": data_id})

        assert len(data) == 1

    async def test_ManyObjects_test_set_options(self) -> None:
        crudOptions: CrudOptions = CrudOptions("PROJECT", "USER")
        oldCrudOptions: CrudOptions = copy.deepcopy(self.many.handlerCrudMany.options)
        self.many.set_crud_options(crudOptions)
        assert self.many.handlerCrudMany.options.projectId == "PROJECT"
        assert self.many.handlerCrudMany.options.userId == "USER"
        self.many.set_crud_options(oldCrudOptions)

    async def test_ManyObjects_get_single(self) -> None:
        data_id = ObjectId()
        await self.test_ManyObjects_insertUpdate(data_id)
        data = await self.many.get_single(**{"_id": data_id})

        assert data["_id"] == data_id

    async def test_ManyObjects_get_by_id(self) -> None:
        data_id = ObjectId()
        await self.test_ManyObjects_insertUpdate(data_id)

        data = await self.many.get_by_id(data_id)
        assert data["code"] == 1

    async def test_ManyObjects_get_with_limit(self) -> None:
        data_id = ObjectId()
        await self.test_ManyObjects_insertUpdate(data_id)

        data = await self.many.get_with_limit(limit=1, **{"_id": data_id})
        assert len(data) == 1

    async def test_ManyObjects_get_error_str(self) -> None:
        self.many.errors = ["Error"]
        assert self.many.get_errors() == ["Error"]

    async def test_ManyObjects_delete_hard_nop_validation(self) -> None:
        data_id = ObjectId()
        await self.test_ManyObjects_insertUpdate(data_id)
        await self.many.delete_after_validation()

        tr.translate("MSG_SUCCESSFULLY_HARD_DELETED")[
            :-2
        ] == self.many.handlerCrudMany.get_messages()

    async def test_ManyObjects_reset_errors(self) -> None:
        self.many.errors = ["Errors"]
        self.many.reset_errors()
        assert not self.many.errors

    async def test_ManyObjects_translate(self) -> None:
        self.many.set_language("en")
        self.many.translate("MSG_SUCCESSFULLY_INSERTED")

        assert self.many.translate("MSG_SUCCESSFULLY_INSERTED") == tr.translate(
            "MSG_SUCCESSFULLY_INSERTED"
        )

    async def test_ManyObjects_get_errors_no_crud(self) -> None:
        mock2 = mc.MockManyObjects()
        mock2.errors.append("Error")
        assert len(mock2.get_errors()) == 1
        assert mock2.get_errors()[0] == "Error"

    async def test_ManyObjects_get_errors_with_crud(self) -> None:
        mock2 = mc.MockManyObjects()
        mock2.errors.append("Error")
        mock2.set_crud(mongo_db)
        mock2.handlerCrudMany.errors.append("Error2")
        assert len(mock2.get_errors()) == 2
        assert mock2.get_errors()[0] == "Error"
        assert mock2.get_errors()[1] == "Error2"

    async def test_ManyObjects_get_messages_no_crud(self) -> None:
        mock2 = mc.MockManyObjects()
        mock2.messages.append("Message")
        assert len(mock2.get_messages()) == 1
        assert mock2.get_messages()[0] == "Message"

    async def test_ManyObjects_get_messages_with_crud(self) -> None:
        mock2 = mc.MockManyObjects()
        mock2.messages.append("Message")
        mock2.set_crud(mongo_db)
        mock2.handlerCrudMany.messages.append("Message2")
        assert len(mock2.get_messages()) == 2
        assert mock2.get_messages()[0] == "Message"
        assert mock2.get_messages()[1] == "Message2"

    async def test_ManyObjects_get_data_no_crud(self) -> None:
        mock2 = mc.MockManyObjects()
        mock2.data.append({"one": 1})
        assert len(mock2.get_data()) == 1
        assert mock2.get_data()[0] == {"one": 1}

    async def test_ManyObjects_get_data_with_crud(self) -> None:
        mock2 = mc.MockManyObjects()
        mock2.data.append({"one": 1})
        mock2.set_crud(mongo_db)
        mock2.handlerCrudMany.data.append({"one": 2})
        assert len(mock2.get_data()) == 2
        assert mock2.get_data()[0] == {"one": 1}
        assert mock2.get_data()[1] == {"one": 2}

    async def test_ManyObjects_bulk(self) -> None:
        mock3 = mc.MockManyObjects()
        mock3.set_bulk_upload(True)

        assert mock3._is_bulk_upload()

    async def test_ManyObjects_bulk_false(self) -> None:
        mock3 = mc.MockManyObjects()
        mock3.set_bulk_upload(False)

        assert not mock3._is_bulk_upload()


class TestReturnMutation:
    async def test_ManyObjects_return_mutation_only_valid(self) -> None:

        mock4 = mc.MockManyObjects()
        mock4.validSchemas = [{"id": 2}]
        mock4.messages = ["Test"]
        mock4.data = [{"id": 2}]

        result = mock4.return_mutation()
        assert result.code == 200
        assert result.messages == ["Test"]
        assert not result.errors
        assert result.data == [{"id": 2}]

    async def test_ManyObjects_return_mutation_only_invalid(self) -> None:

        mock5 = mc.MockManyObjects()
        mock5.inValidSchemas = [{"id": 2}]
        mock5.errors = ["Error"]

        result = mock5.return_mutation()
        assert result.code == 400
        assert not result.messages
        assert result.errors == ["Error"]
        assert not result.data

    async def test_ManyObjects_return_mutation_valid_and_invalid(self) -> None:

        mock6 = mc.MockManyObjects()
        mock6.validSchemas = [{"id": 2}]
        mock6.inValidSchemas = [{"id": 2}]
        mock6.messages = ["Test"]
        mock6.errors = ["Error"]
        mock6.data = [{"id": 2}]

        result = mock6.return_mutation()
        assert result.code == 400
        assert result.messages == ["Test"]
        assert result.errors == ["Error"]
        assert result.data == [{"id": 2}]

    async def test_ManyObjects_return_mutation_not_valid_and_not_invalid_200(self) -> None:

        mock7 = mc.MockManyObjects()

        result = mock7.return_mutation()
        assert result.code == 200
        assert not result.messages
        assert not result.errors
        assert not result.data

    async def test_ManyObjects_return_mutation_not_valid_and_not_invalid_500(self) -> None:

        mock8 = mc.MockManyObjects()
        mock8.errors = ["Error"]

        result = mock8.return_mutation()
        assert result.code == 500
        assert not result.messages
        assert result.errors == ["Error"]
        assert not result.data


def assertUpdateMany(
    crud: CrudMany,
    httpCode: HTTPCode,
    httpCodes: List[HTTPCode],
    messages: List[str],
    auditFields: List[List[str]],
) -> None:
    assertComonUpdateMany(crud, httpCode, httpCodes)
    for idx, modifiedData in enumerate(crud.get_data()):
        assertAuditFieldsUpdateMany(modifiedData, auditFields[idx])
    for idx, message in enumerate(messages):
        assertMessageUpdateMany(crud.get_messages()[idx], message)


def assertComonUpdateMany(crud: CrudMany, httpCode: HTTPCode, httpCodes: List[HTTPCode]) -> None:
    assert crud.http_code == httpCode
    assert crud.http_codes == httpCodes


def assertAuditFieldsUpdateMany(modifiedData: TData, auditFields: List[str]) -> None:
    if CREATE in auditFields:
        assert CREATE_DATE in modifiedData
        assert CREATE_USER in modifiedData
    else:
        assert CREATE_DATE not in modifiedData
        assert CREATE_USER not in modifiedData
    if UPDATE in auditFields:
        assert MODIFIED_DATE in modifiedData
        assert MODIFIED_USER in modifiedData
    else:
        assert MODIFIED_DATE not in modifiedData
        assert MODIFIED_USER not in modifiedData
    if DELETE in auditFields:
        assert DELETED_DATE in modifiedData
        assert DELETED_USER in modifiedData
    else:
        assert DELETED_DATE not in modifiedData
        assert DELETED_USER not in modifiedData


def assertMessageUpdateMany(savedMessage: str, message: str) -> None:
    assert tr.translate(message)[:-2] in savedMessage


class TestErrors:
    def test_error_ErrorBase(self) -> None:
        with pytest.raises(err.ErrorBase):
            raise err.ErrorBase("Error")

    def test_error_ErrorEmptyData(self) -> None:
        with pytest.raises(err.ErrorEmptyData):
            raise err.ErrorEmptyData("Error")

    def test_error_ErrorDuplicatedField(self) -> None:
        with pytest.raises(err.ErrorDuplicatedField):
            raise err.ErrorDuplicatedField("Error")

    def test_error_ErrorInvalidID(self) -> None:
        with pytest.raises(err.ErrorInvalidID):
            raise err.ErrorInvalidID("Error")

    def test_error_ErrorUniqueCode(self) -> None:
        with pytest.raises(err.ErrorUniqueCode):
            raise err.ErrorUniqueCode("Error")

    def test_error_ErrorAlreadyProvided(self) -> None:
        with pytest.raises(err.ErrorAlreadyProvided):
            raise err.ErrorAlreadyProvided("Error")

    def test_error_ErrorNonexistingData(self) -> None:
        with pytest.raises(err.NonexistingData):
            raise err.NonexistingData("Error")
