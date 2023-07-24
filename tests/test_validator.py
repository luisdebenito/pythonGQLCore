from _python_core.validator.RequiredField import RequiredField
from _python_core.validator.dateValidator import IsIsoFormatDate
from _python_core.validator.matchType import MatchType
from _python_core.validator.IsValidDependency import (
    IsValidDependency,
)

import _python_core.Errors as err
from _python_core.validator.IsAttributeUsed import IsAttributeUsed
from _python_core.validator.duplicatedFields import DuplicatedField
from _python_core.validator.missingField import MissingField
from _python_core.validator.ExistInDatabase import ExistInDatabase
from _python_core.validator.IsEmpty import IsEmpty
from _python_core.validator.validator import (
    Validator,
    translate,
    translate_format_from_args,
)
from _python_core.crud.crud_options import CrudOptions
from conftest import mongo_db
import os
import sys
from typing import List
from mongomock import ObjectId

import pytest

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))


PROJECTID = "1234"
USER = "user"

validator = Validator()
validator.set_crud(mongo_db)
validator.set_crud_options(CrudOptions(PROJECTID, USER))
validator.set_collection("Test")


class Test_IsEmpty:
    isEmpty = IsEmpty(validator)

    def test_empty(self) -> None:
        with pytest.raises(err.ErrorValidatorEmpty) as excinfo:
            self.isEmpty.validate({})
        assert str(excinfo.value) == translate("ERROR_EMPTY_DATA", {}, "en")

    def test_not_empty(self) -> None:
        assert self.isEmpty.validate({"test": 1}) is False


class Test_ExistInDatabase:
    existInDDBB = ExistInDatabase(validator)

    async def test_exist_in_database_raise_exception(self) -> None:
        data_id: str = str(ObjectId())

        with pytest.raises(err.ErrorValidatorExistInDatabase) as excinfo:
            await self.existInDDBB.validate(data_id)

        assert str(excinfo.value) == translate("ERROR_DELETE_NONEXISTING", lang="en")

    async def test_exist_in_database_not_raise_exception(self) -> None:
        data_id: ObjectId = ObjectId()
        mongo_db["Test"].insert_one({"_id": data_id})

        await self.existInDDBB.validate(data_id) is True


class Test_MissingField:
    missingField = MissingField(validator)

    def test_missing_field(self) -> None:
        with pytest.raises(err.ErrorValidatorMissingField) as excinfo:
            self.missingField.validate({"one": 1}, "two")
        assert str(excinfo.value) == translate_format_from_args("ERROR_MISSING_FIELD", "en", "two")

    def test_not_missing_field(self) -> None:
        assert self.missingField.validate({"test": 1}, "test") is False


class Test_MatchType:
    matchType = MatchType(validator)

    def test_not_match_int_str(self) -> None:
        with pytest.raises(err.ErrorMatchType) as excinfo:
            self.matchType.validate(123, "str", "code")
        assert str(excinfo.value) == translate_format_from_args(
            "ERROR_TYPE_FIELD",
            "en",
            "str",
            "int",
            "code",
        )

    def test_not_match_int_bool(self) -> None:
        with pytest.raises(err.ErrorMatchType) as excinfo:
            self.matchType.validate(123, "bool", "code")
        assert str(excinfo.value) == translate_format_from_args(
            "ERROR_TYPE_FIELD",
            "en",
            "bool",
            "int",
            "code",
        )

    def test_not_match_str_bool(self) -> None:
        with pytest.raises(err.ErrorMatchType) as excinfo:
            self.matchType.validate("test", "bool", "code")
        assert str(excinfo.value) == translate_format_from_args(
            "ERROR_TYPE_FIELD",
            "en",
            "bool",
            "str",
            "code",
        )

    def test_match_str(self) -> None:
        assert self.matchType.validate("string", "str", "code")

    def test_match_bool(self) -> None:
        assert self.matchType.validate(True, "bool", "code")

    def test_match_int(self) -> None:
        assert self.matchType.validate(123, "int", "code")

    def test_match_float(self) -> None:
        assert self.matchType.validate(123.5, "float", "code")

    def test_match_int_float(self) -> None:
        assert self.matchType.validate(123, "float", "code")


class Test_IsoFormatDate:
    isIsoformatDate = IsIsoFormatDate(validator)

    def test_not_isoformat_date_DDMMYYYY(self) -> None:
        with pytest.raises(err.ErrorValidatorIsIsoFormatDate) as excinfo:
            self.isIsoformatDate.validate("20-02-1999")
        assert str(excinfo.value) == translate("ERROR_DATE_FORMAT")

    def test_not_isoformat_date_MMDDYYYY(self) -> None:
        with pytest.raises(err.ErrorValidatorIsIsoFormatDate) as excinfo:
            self.isIsoformatDate.validate("02-02-1999")
        assert str(excinfo.value) == translate("ERROR_DATE_FORMAT")

    def test_not_isoformat_date_YYYYDDMM(self) -> None:
        with pytest.raises(err.ErrorValidatorIsIsoFormatDate) as excinfo:
            self.isIsoformatDate.validate("1999-20-02")
        assert str(excinfo.value) == translate("ERROR_DATE_FORMAT")

    def test_not_isoformat_date_random_type(self) -> None:
        with pytest.raises(err.ErrorValidatorIsIsoFormatDate) as excinfo:
            self.isIsoformatDate.validate("random_characters")
        assert str(excinfo.value) == translate("ERROR_DATE_FORMAT")

    def test_is_isoformat_date_YYYYMMDD_wrong_date(self) -> None:
        with pytest.raises(err.ErrorValidatorIsIsoFormatDate) as excinfo:
            self.isIsoformatDate.validate("1999-11-31")
        assert str(excinfo.value) == translate("ERROR_DATE_FORMAT")

    def test_is_isoformat_date_YYYYMMDD(self) -> None:
        assert self.isIsoformatDate.validate("1999-02-20")

    def test_is_isoformat_date_YYYYMMDDhhmmss(self) -> None:
        assert self.isIsoformatDate.validate("2022-09-28T00:00:00.000Z")


class Test_RequiredField:
    requiredField = RequiredField(validator)

    def test_name_required_null_provided(self) -> None:
        with pytest.raises(err.ErrorValidatorRequiredField) as excinfo:
            self.requiredField.validate({"name": None, "surname": "Shelby"}, "name")
        assert str(excinfo.value) == translate_format_from_args("ERROR_REQUIRED_FIELD", "en", "name")  # fmt: skip

    def test_name_required_empty_provided(self) -> None:
        with pytest.raises(err.ErrorValidatorRequiredField) as excinfo:
            self.requiredField.validate({"name": "", "surname": "Shelby"}, "name")
        assert str(excinfo.value) == translate_format_from_args("ERROR_REQUIRED_FIELD", "en", "name")  # fmt: skip

    def test_name_required_empty_array_provided(self) -> None:
        with pytest.raises(err.ErrorValidatorRequiredField) as excinfo:
            self.requiredField.validate({"name": [], "surname": "Shelby"}, "name")
        assert str(excinfo.value) == translate_format_from_args("ERROR_REQUIRED_FIELD", "en", "name")  # fmt: skip

    def test_name_required_not_in_schema(self) -> None:
        with pytest.raises(err.ErrorValidatorRequiredField) as excinfo:
            self.requiredField.validate({"surname": "Shelby"}, "name")
        assert str(excinfo.value) == translate_format_from_args("ERROR_REQUIRED_FIELD", "en", "name")  # fmt: skip

    def test_surname_required(self) -> None:
        assert self.requiredField.validate({"surname": "Shelby"}, "surname")  # fmt: skip

    def test_number_required(self) -> None:
        assert self.requiredField.validate({"number": 0}, "number")  # fmt: skip

    def test_number_required_None(self) -> None:
        with pytest.raises(err.ErrorValidatorRequiredField) as excinfo:
            self.requiredField.validate({"number": None}, "number")
        assert str(excinfo.value) == translate_format_from_args("ERROR_REQUIRED_FIELD", "en", "number")  # fmt: skip

    def test_bool_required_True(self) -> None:
        assert self.requiredField.validate({"isValid": True}, "isValid")  # fmt: skip

    def test_bool_required_False(self) -> None:
        assert self.requiredField.validate({"isValid": False}, "isValid")  # fmt: skip

    def test_bool_required_None(self) -> None:
        with pytest.raises(err.ErrorValidatorRequiredField) as excinfo:
            self.requiredField.validate({"isValid": None}, "isValid")
        assert str(excinfo.value) == translate_format_from_args("ERROR_REQUIRED_FIELD", "en", "isValid")  # fmt: skip


class Test_DuplicateFields:
    duplicateFields = DuplicatedField(validator)

    async def test_duplicateFields(self) -> None:
        mongo_db["Test"].insert_one({"one": 1, "two": 2, "projectId": PROJECTID})

        with pytest.raises(err.ErrorValidatorDuplicatedField) as excinfo:
            await self.duplicateFields.validate([("one", 1), ("two", 2)])
        assert str(excinfo.value) == translate("ERROR_DUPLICATE_ALREADY_EXIST",{f[0]: f[1] for f in [("one", 1), ("two", 2)]},lang="en")  # fmt: skip

    async def test_no_duplicated(self) -> None:
        mongo_db["Test"].insert_one({"one": 1, "two": 2, "projectId": PROJECTID})

        await self.duplicateFields.validate([("three", 3)]) is True

    async def test_no_duplicated_matching_one(self) -> None:
        mongo_db["Test"].insert_one({"one": 1, "two": 2, "project": {"id": PROJECTID}})

        with pytest.raises(err.ErrorValidatorDuplicatedField) as excinfo:
            await self.duplicateFields.validate([("one", 1)])
        assert str(excinfo.value) == translate("ERROR_DUPLICATE_ALREADY_EXIST", {f[0]: f[1] for f in [("one", 1)]}, lang="en")  # fmt: skip

    async def test_no_duplicated_empty(self) -> None:
        mongo_db["Test"].insert_one({"one": 1, "two": 2, "projectId": PROJECTID})

        await self.duplicateFields.validate([]) is True

    async def test_no_duplicated_matching_key(self) -> None:
        mongo_db["Test"].insert_one({"one": 1, "two": 2, "projectId": PROJECTID})

        await self.duplicateFields.validate([("one", 3)]) is True


class Test_IsAttributeUsed:
    async def test_is_attribute_used(self, my_mongos: List) -> None:
        isAttributeUsed = IsAttributeUsed(validator)
        mongo_db["Test"].insert_one({"one": 1, "projectId": PROJECTID, "active": True})
        query = {"projectId": PROJECTID, "active": True}
        mongo = my_mongos[0]["test"]
        with pytest.raises(err.ErrorValidatorIsAttributeUsed) as excinfo:
            await isAttributeUsed.validate("Test", query, 0, mongo)
        assert str(excinfo.value) == translate("ERROR_IS_ATTRIBUTE_USED", "Test", "en")

    # FIXME: uncomment when validate_with_gql is fixed
    # async def test_is_attribute_used_gql(self, my_mongos: List) -> None:
    #     isAttributeUsed = IsAttributeUsed(validator)
    #     with pytest.raises(err.ErrorValidatorIsAttributeUsed) as excinfo:
    #         await isAttributeUsed.validate_with_gql("", {}, {}, "resource", 0)
    #     assert str(excinfo.value) == translate("ERROR_IS_ATTRIBUTE_USED", "resource", "en")

    async def test_not_is_attribute_used(self, my_mongos: List) -> None:
        isAttributeUsed = IsAttributeUsed(validator)
        query = {"projectId": PROJECTID, "active": True}
        mongo = my_mongos[0]["test"]
        assert await isAttributeUsed.validate("Test1", query, 0, mongo) is True

    # FIXME: uncomment when validate_with_gql is fixed
    # async def test_not_is_attribute_used_gql(self, my_mongos: List) -> None:
    #     isAttributeUsed = IsAttributeUsed(validator)
    #     assert await isAttributeUsed.validate_with_gql("", {}, {}, "user", 0) is True

    async def test_not_is_attribute_used_other_database(self, my_mongos: List) -> None:
        isAttributeUsed = IsAttributeUsed(validator)
        query = {"projectId": PROJECTID, "active": True}
        mongo = my_mongos[0]["other"]
        assert await isAttributeUsed.validate("Test1", query, 0, mongo) is True

    async def test_is_attribute_used_other_database(self, my_mongos: List) -> None:
        isAttributeUsed = IsAttributeUsed(validator)
        query = {"projectId": PROJECTID, "active": True}
        mongo = my_mongos[0]["other"]
        mongo["Other"].insert_one({"one": 1, "projectId": PROJECTID, "active": True})
        with pytest.raises(err.ErrorValidatorIsAttributeUsed) as excinfo:
            await isAttributeUsed.validate("Other", query, 0, mongo)
        assert str(excinfo.value) == translate("ERROR_IS_ATTRIBUTE_USED", "Other", "en")


class Test_ValidatorValidValue:
    validValueSpecificField = IsValidDependency(validator)

    def test_invalid_value_for_company_id(self) -> None:
        with pytest.raises(err.ErrorValidatorValidDependency) as excinfo:
            self.validValueSpecificField.validate(None, "company")
        assert str(excinfo.value) == translate_format_from_args("ERROR_INVALID_VALUE_FOR_SPECIFIC_FIELD","en","company")  # fmt: skip

    def test_invalid_value_for_company_id_null(self) -> None:
        with pytest.raises(err.ErrorValidatorValidDependency) as excinfo:
            self.validValueSpecificField.validate(None, "company")
        assert str(excinfo.value) == translate_format_from_args("ERROR_INVALID_VALUE_FOR_SPECIFIC_FIELD","en","company")  # fmt: skip

    def test_invalid_value_for_company_id_invalid(self) -> None:
        with pytest.raises(err.ErrorValidatorValidDependency) as excinfo:
            self.validValueSpecificField.validate("000000000000000000000000", "company")
        assert str(excinfo.value) == translate_format_from_args("ERROR_INVALID_VALUE_FOR_SPECIFIC_FIELD","en","company")  # fmt: skip

    def test_valid_value_for_company_id(self) -> None:
        assert self.validValueSpecificField.validate("619f548cab62a38ec56d9468", "company")
