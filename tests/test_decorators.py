import os
import sys
from typing import Any, Dict, List, Tuple
from graphql import GraphQLError
from _python_core.constants import CURRENT_LANG
import pytest
from conftest import mongo_db

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core import decorators
from _python_core.http_codes import HTTPCode
from _python_core.responseGQL import ResponseGQL

# Kurt USERID
USER = "02477c69-56f4-4e77-921a-23a2a82a335e"
PROJECT_ID = "12070c789f30472094bbcf61923ecab4"
SERVICE = "service"
READ = "read"
WRITE = "write"
DELETE = "delete"

data = {"test": 1}


class A1:
    class A2:
        scope = {"user_id": USER, "authorization": f"{PROJECT_ID}:{SERVICE}:{WRITE}"}
        headers = {CURRENT_LANG: "de"}

    context = {"request": A2}


@decorators.return_mutation_resolver([(SERVICE, [WRITE])], mongo_db)
async def func_mutation(data: Dict, projectId: str, **kwargs: Any) -> Tuple[List[str], List[Dict]]:
    return ResponseGQL(HTTPCode.CODE_200, messages=["test"], data=[data])


@decorators.return_mutation_resolver([(SERVICE, [WRITE])], mongo_db)
async def func_mutation_with_exception(
    data: Dict, projectId: str, **kwargs: Any
) -> Tuple[List[str], List[Dict]]:
    raise RuntimeError("Error")


@decorators.return_mutation_resolver([(SERVICE, [WRITE])], mongo_db)
async def func_mutation_with_exception_with_ddbb(
    data: Dict, projectId: str, **kwargs: Any
) -> Tuple[List[str], List[Dict]]:
    raise RuntimeError("Error_test_with_ddbb")


@decorators.return_mutation_resolver([(SERVICE, [WRITE])])
async def func_mutation_with_exception_with_no_ddbb(
    data: Dict, projectId: str, **kwargs: Any
) -> Tuple[List[str], List[Dict]]:
    raise RuntimeError("Error_test_with_no_ddbb")


@decorators.return_query_resolver([(SERVICE, [WRITE])], mongo_db)
async def func_query(data: Dict, projectId: str, **kwargs: Any) -> Dict:
    return data


@decorators.return_query_resolver([(SERVICE, [WRITE])], mongo_db)
async def func_query_with_exception(data: Dict, projectId: str, **kwargs: Any) -> Dict:
    raise IndexError("Error")


@decorators.return_query_resolver_no_auth()
async def func_query_no_auth(data: Dict, projectId: str, **kwargs: Any) -> Dict:
    return data


@decorators.return_query_resolver_no_auth()
async def func_query_no_auth_with_exception(data: Dict, projectId: str, **kwargs: Any) -> Dict:
    raise IndentationError("Error")


kwargs: Dict[str, Any] = {"data": data, "projectId": PROJECT_ID}
noProjectKwargs: Dict[str, Any] = {"data": data, "projectId": ""}


class TestDecoratorsMutation:
    async def test_mutation_resolver_ok(self) -> None:
        """Test return mutation"""
        res: ResponseGQL = await func_mutation("", A1, **kwargs)
        assertResponseCode(res, HTTPCode.CODE_200, ["test"], [], [data])

    async def test_mutation_resolver_ko_auth_reject(self) -> None:
        """Test return mutation"""

        class Info_Auth_Reject:
            class A2:
                scope = {
                    "user_id": USER,
                    "authorization": "1" + ":" + SERVICE + ":" + WRITE,
                }
                headers = {CURRENT_LANG: "de"}

            context = {"request": A2}

        res: ResponseGQL = await func_mutation("", Info_Auth_Reject, **kwargs)
        assertResponseCode(res, HTTPCode.CODE_401, [], ["Auth rejected"], [])

    async def test_catch_exception_mutation(self) -> None:
        res: ResponseGQL = await func_mutation_with_exception("", A1, **kwargs)
        assertResponseCode(res, HTTPCode.CODE_500, [], ["Error"], [])


class TestDecoratorsQueryWithAuth:
    async def test_query_resolver_ok(self) -> None:
        res = await func_query("", A1, **kwargs)
        assert res == data

    async def test_query_resolver_ko_auth_reject(self) -> None:
        class Info_Auth_Reject:
            class A2:
                scope = {
                    "user_id": USER,
                    "authorization": "1" + ":" + SERVICE + ":" + WRITE,
                }
                headers = {CURRENT_LANG: "de"}

            context = {"request": A2}

        with pytest.raises(GraphQLError) as ex:
            await func_query("", Info_Auth_Reject, **kwargs)

        assert str(ex.value) == "Auth rejected"

    async def test_catch_exception_query(self) -> None:
        with pytest.raises(Exception) as excinfo:
            await func_query_with_exception("", A1, **kwargs)

        assert str(excinfo.value) == "Error"

    async def test_query_resolver_ok_project_in_headers(self) -> None:
        class A1:
            class A2:
                scope = {"user_id": USER, "authorization": f"{PROJECT_ID}:{SERVICE}:{WRITE}"}
                headers = {"projectid": PROJECT_ID}

            context = {"request": A2}

        res = await func_query("", A1, **noProjectKwargs)
        assert res == data

    async def test_query_resolver_ko_project_non_existing(self) -> None:
        class A1:
            class A2:
                scope = {"user_id": USER, "authorization": f"{PROJECT_ID}:{SERVICE}:{WRITE}"}
                headers = {"projectid": ""}

            context = {"request": A2}

        with pytest.raises(GraphQLError) as ex:
            await func_query("", A1, **noProjectKwargs)

        assert str(ex.value) == "Auth rejected"


class TestDecoratorsQueryWithNoAuth:
    async def test_query_resolver_no_auth(self) -> None:
        res = await func_query_no_auth("", A1, **kwargs)
        assert res == data

    async def test_catch_exception_query_no_auth(self) -> None:
        with pytest.raises(Exception) as excinfo:
            await func_query_no_auth_with_exception("", A1, **kwargs)

        assert str(excinfo.value) == "Error"


class TestErrorSaveInDatabase:
    async def test_query_error_mutation_save_in_ddbb(self) -> None:
        await func_mutation_with_exception_with_ddbb("", A1, **kwargs)
        assert mongo_db["Error"].find_one({"_error": "Error_test_with_ddbb"})

    async def test_query_error_mutation_dont_save_in_ddbb(self) -> None:
        await func_mutation_with_exception_with_no_ddbb("", A1, **kwargs)
        assert mongo_db["Error"].find_one({"_error": "Error_test_with_no_ddbb"}) is None


def assertResponseCode(
    res: ResponseGQL, code: HTTPCode, messages: List, errors: List, data: List
) -> None:
    assert res.code == code
    assert res.messages == messages
    assert res.errors == errors
    assert res.data == data


@decorators.return_query_resolver([(SERVICE, [WRITE])], mongo_db)
@decorators.set_crudOptions_for_resolvers()
async def func_query_with_crudOptions_in_resolvers(
    data: Dict, projectId: str, **kwargs: Any
) -> Dict:
    return {
        "diary": {
            "else": {"else": "else"},
            "project": {"id": "65c5351a731a4a4e9edef462c75284a0"},
            "idNMore": {"id": "65c5351a731a4a4e9edef462c75284a0", "more": "peep"},
            "timecard": {"resourceActivities": [{"resource": {"id": "validId"}}]},
        }
    }


class TestCrudOptionsInReferences:
    async def test_query_ok_with_crudOptions_in_resolvers(self) -> None:
        """Test data is filled with crudOptions in the references"""
        kwargs["crudOptions"] = {"just": "testing"}
        data: Dict = await func_query_with_crudOptions_in_resolvers("", A1, **kwargs)
        assert data["diary"]
        assert data["diary"]["project"].get("crudOptions") == kwargs["crudOptions"]
        assert (
            data["diary"]["timecard"]["resourceActivities"][0]["resource"].get("crudOptions")
            == kwargs["crudOptions"]
        )
        assert not data["diary"]["idNMore"].get("crudOptions")
        assert not data["diary"]["else"].get("crudOptions")
