import copy
import json
import logging
import sys
from typing import Any, Dict, List

from graphql.type.definition import GraphQLResolveInfo
from mongomock import MongoClient

from _python_core.crud.crud_options import CrudOptions
from _python_core.crud.crud_single import CrudOne
from _python_core.constants import (
    INFO,
    PROJECTID,
    REQUEST,
    AUTHORIZATION,
    COLLECTION_ERROR,
    HEADERS,
    SCOPE,
    BODY,
)
from _python_userauthorization.ariadne import get_user_id

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(levelname)s:\t  %(message)s",
)


class Collections:
    ERROR = COLLECTION_ERROR


class TraceBack:

    # Attributes
    headers: Dict[str, Any] = {}
    scope: Dict[str, Any] = {}
    body: str = ""
    error: str = ""
    traceback: List[str] = []
    stack: List[str] = []
    ddbb: CrudOne = None
    # Generic
    info = None
    request = None
    projectId = None
    # User
    token = None
    userId = None

    @staticmethod
    def set_data(args: Dict[str, Any]) -> None:
        TraceBack.resetValues()
        TraceBack.info = args[INFO]
        TraceBack.projectId = args[PROJECTID]
        TraceBack.userId = get_user_id(args[INFO].context)
        for i in args:
            if isinstance(args[i], GraphQLResolveInfo) and REQUEST in args[i].context.keys():
                TraceBack._getHeaders(args[i].context[REQUEST].headers)
                TraceBack.token = args[i].context[REQUEST].headers.get(AUTHORIZATION)
                TraceBack._getBody(args[i].context[REQUEST]._body)
                TraceBack.request = args[i].context[REQUEST]
                TraceBack._getScope(args[i].context[REQUEST].scope)

    @staticmethod
    def _getHeaders(headers: Any) -> None:
        """Gets Header Request"""
        for i in headers.raw:
            if isinstance(i, tuple):
                try:
                    key = i[0].decode("utf-8")
                    value = i[1].decode("utf-8")
                    TraceBack.headers.update({key: value})
                except Exception as excinfo:
                    logging.error(f"Error to decode header string:{excinfo}")

    @staticmethod
    def _getBody(body: Any) -> None:
        """Gets Body Request"""
        try:
            TraceBack.body = json.loads(body.decode("utf-8"))
        except Exception as excinfo:
            logging.error(f"Error to decode body string:{excinfo}")

    @staticmethod
    def _getScope(scope: Dict[str, Any]) -> None:
        """Gets Scopes from Request"""
        if isinstance(scope, dict):
            for key, value in scope.items():
                if key in ["method", "root_path", "user_id", "roles", "project", PROJECTID]:
                    TraceBack.scope.update({key: value})

    @staticmethod
    def set_crud(ddbb: MongoClient) -> None:
        TraceBack.ddbb = CrudOne(ddbb)
        TraceBack.ddbb.options = CrudOptions(
            TraceBack.projectId, TraceBack.userId
        )
        if ddbb:
            TraceBack.ddbb.set_collection(Collections.ERROR)

    @staticmethod
    def set_Error_and_Traceback(error_msg: str, trace: List[str], stack: List[str]) -> None:
        TraceBack.error = copy.deepcopy(error_msg)
        TraceBack.traceback = copy.deepcopy(trace)
        TraceBack.stack = copy.deepcopy(stack)

    @staticmethod
    async def save_in_database() -> None:
        try:
            if TraceBack.is_deployed():
                await TraceBack.ddbb.insert_update(TraceBack.print())
                inserted_id = TraceBack.ddbb.schema.get("_id", "Unknown id")
                logging.info(f"Error saved in database with id:{inserted_id}")

        except Exception as excinfo:
            logging.error(f"Unkown error when saving trace in ddbb:{excinfo}")

    @staticmethod
    def is_deployed() -> bool:
        logging.info(f"Checking if is deployed:{TraceBack.headers}")
        if TraceBack.headers and TraceBack.headers.get("host"):
            for placeHolder in ["127.0.0.1", "localhost"]:
                if placeHolder in TraceBack.headers["host"]:
                    logging.info(
                        f"Placeholder mactches:{placeHolder} with host:{TraceBack.headers['host']}"
                    )
                    return False
        return True

    @staticmethod
    def print() -> Dict[str, Any]:
        """Return Structure to print"""
        return {
            HEADERS: TraceBack.headers,
            SCOPE: TraceBack.scope,
            BODY: json.dumps(TraceBack.body),
            "_error": TraceBack.error,
            "_traceback": TraceBack.traceback,
            "_stack": TraceBack.stack,
        }

    @staticmethod
    def resetValues() -> None:
        # Attributes
        TraceBack.headers = {}
        TraceBack.scope = {}
        TraceBack.body = ""
        TraceBack.error = ""
        TraceBack.traceback = []
        TraceBack.stack = []
        TraceBack.ddbb = None
        # Generic
        TraceBack.info = None
        TraceBack.request = None
        TraceBack.projectId = None
        # User
        TraceBack.token = None
        TraceBack.userId = None
