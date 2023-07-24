import logging
import sys
import traceback
from functools import wraps
from typing import Any, Dict, List, Tuple

from graphql import GraphQLError
from _python_userauthorization.ariadne import check_authorization
from pymongo import MongoClient

import _python_core.Errors as err
from _python_core.http_codes import HTTPCode
from _python_core.mytraceback import TraceBack
from _python_core.responseGQL import ResponseGQL
from _python_core.constants import (
    CURRENT_LANG,
    DEFAULT_LANG,
    HEADERS,
    ID,
    INFO,
    LANG,
    PARENT,
    REQUEST,
    PROJECTID,
    CRUDOPTIONS,
)


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(levelname)s:\t  %(message)s",
)


def return_mutation_resolver(resources_and_scopes: Any, ddbb: MongoClient = None) -> Any:
    def wrapper(func: Any) -> Any:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Dict) -> Dict[str, Any]:
            # sourcery no-metrics skip: simplify-fstring-formatting
            try:
                kwargs = add_args_to_kwargs(*args, **kwargs)
                kwargs[LANG] = kwargs[INFO].context[REQUEST].headers.get(CURRENT_LANG, DEFAULT_LANG)  # type: ignore
                TraceBack.set_data(kwargs)
                return (
                    await func(**kwargs)
                    if is_authorized(resources_and_scopes, **kwargs)
                    else ResponseGQL(HTTPCode.CODE_401, errors=["Auth rejected"])
                )

            except err.ErrorBase as ex:
                await set_error_for_Resolver(ex)
                return ResponseGQL(HTTPCode.CODE_500, errors=[str(ex)])

            except Exception as ex:
                TraceBack.set_crud(ddbb)
                await set_error_for_Resolver(ex)
                return ResponseGQL(HTTPCode.CODE_500, errors=[str(ex)])

        return wrapped

    return wrapper


def return_query_resolver(resources_and_scopes: Any, ddbb: MongoClient = None) -> Any:
    def wrapper(func: Any) -> Any:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Dict) -> Dict:
            # sourcery no-metrics skip: raise-specific-error, simplify-fstring-formatting
            try:
                kwargs = add_args_to_kwargs(*args, **kwargs)
                kwargs[LANG] = kwargs[INFO].context[REQUEST].headers.get(CURRENT_LANG, DEFAULT_LANG)  # type: ignore
                TraceBack.set_data(kwargs)
                return (
                    await func(**kwargs)
                    if is_authorized(resources_and_scopes, **kwargs)
                    else raise_gql_error("Auth rejected")  # type: ignore
                )

            except (err.ErrorBase, GraphQLError) as ex:
                await set_error_for_Resolver(ex)
                raise GraphQLError(str(ex)) from ex

            except Exception as ex:
                TraceBack.set_crud(ddbb)
                await set_error_for_Resolver(ex)
                raise RuntimeError(str(ex)) from ex

        return wrapped

    return wrapper


def return_query_resolver_no_auth(ddbb: MongoClient = None) -> Any:
    def wrapper(func: Any) -> Any:
        @wraps(func)
        async def wrapped(*args: List, **kwargs: Dict) -> Any:
            # sourcery skip: raise-specific-error
            try:
                kwargs = add_args_to_kwargs(*args, **kwargs)
                TraceBack.set_data(kwargs)
                return await func(**kwargs)

            except err.ErrorBase as ex:
                await set_error_for_Resolver(ex)
                raise RuntimeError(str(ex)) from ex

            except Exception as ex:
                TraceBack.set_crud(ddbb)
                await set_error_for_Resolver(ex)
                raise RuntimeError(str(ex)) from ex

        return wrapped

    return wrapper


def raise_gql_error(exception: str) -> None:
    raise GraphQLError(exception)


async def set_error_for_Resolver(ex: Exception) -> None:
    TraceBack.set_Error_and_Traceback(
        str(ex), traceback.format_exc().split("\n"), traceback.format_stack()
    )

    logging.error(f"Error Message:{str(ex)}")

    if TraceBack.ddbb:
        await TraceBack.save_in_database()
        # logging.error(pformat(TraceBack.print()))


def is_authorized(resources_and_services: List[Tuple[str, List[str]]], **kwargs: Dict) -> bool:
    info = kwargs[INFO]
    projectId = get_project_id(info.context, **kwargs)  # type: ignore
    scopes: List[Tuple[str, List[str]]] = []
    for item in resources_and_services:
        scopes.extend(f"{item[0]}:{scope}" for scope in item[1])  # type: ignore
    return bool(projectId and check_authorization(projectId, info.context, scopes))  # type: ignore


def get_project_id(context: Any, **kwargs: Dict) -> str:
    try:
        return get_project_from_headers(context)
    except Exception:
        return get_project_from_arguments(**kwargs)


def get_project_from_headers(context: Any) -> str:
    projectId = context[REQUEST].headers.get("projectid", "")
    assert bool(projectId)
    return projectId


def get_project_from_arguments(**kwargs: Dict[str, Any]) -> str:
    return kwargs.get(PROJECTID, "")  # type: ignore


def add_args_to_kwargs(*args: Any, **kwargs: Dict) -> Dict:
    kwargs[PARENT] = args[0]
    kwargs[INFO] = args[1]
    return kwargs


def find_in_headers_context(request: Any, field: str) -> str | None:
    return (
        next(
            (
                item[1].decode("utf-8")
                for item in request.context[REQUEST].headers.raw
                if item[0].decode("utf-8") == field
            ),
            None,
        )
        if all(
            [
                hasattr(request, "context"),
                request.context.get(REQUEST),
                hasattr(request.context[REQUEST], HEADERS),
                hasattr(request.context[REQUEST].headers, "raw"),
            ]
        )
        else None
    )


def set_crudOptions_for_resolvers() -> Any:
    def wrapper(func: Any) -> Any:
        @wraps(func)
        async def wrapped(**kwargs: Dict) -> Dict[str, Any]:
            data = await func(**kwargs)
            _set_value_in_resolver_fields(data, CRUDOPTIONS, kwargs.get(CRUDOPTIONS, {}))
            return data

        return wrapped

    return wrapper


def _set_value_in_resolver_fields(data: dict | list, valueKey: str, value: Any) -> None:
    if isinstance(data, list):
        for item in data:
            _set_value_in_resolver_fields(item, valueKey, value)
    elif isinstance(data, dict):
        if _is_object_reference(data):
            data[valueKey] = value
        else:
            for _val in data.values():
                if isinstance(_val, (dict, list)):
                    _set_value_in_resolver_fields(_val, valueKey, value)


def _is_object_reference(element: Any) -> bool:
    return _is_object_reference_by_id(element)


def _is_object_reference_by_id(element: Dict) -> bool:
    return len(element.keys()) == 1 and isinstance(element.get(ID), str)
