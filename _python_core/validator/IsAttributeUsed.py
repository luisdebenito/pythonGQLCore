from typing import Dict

from mongomock import Database

import _python_core.Errors as err
from _python_core.crud.crud_single import CrudOne
from _python_core.validator.validator import Validator, translate

# FIXME: problems with python 3.10
# from _python_core.graphqlClient import IGraphqlClient


class IsAttributeUsed(Validator):
    def __init__(self, validator: Validator):
        self.lang: str = validator.lang
        self.crud = validator.crud

    async def validate(
        self, collection: str, query: Dict, repeated: int, ddbb: Database = None
    ) -> bool:
        ddbb = ddbb if ddbb else self.crud.mongoDB
        crud = CrudOne(ddbb, self.lang)
        crud.set_collection(collection)
        data = await crud.get(**query)

        if len(data) == repeated:
            return True
        raise err.ErrorValidatorIsAttributeUsed(
            translate("ERROR_IS_ATTRIBUTE_USED", collection, lang=self.lang)
        )

    # FIXME: problems with python 3.10
    # async def validate_with_gql(
    #     self,
    #     query: str,
    #     variables: Dict,
    #     headers: Dict,
    #     field: str,
    #     repeated: int,
    #     federation_url: str = None,
    # ) -> bool:

    #     graphql_client = IGraphqlClient(federation_url).graphql_client
    #     data = await graphql_client.execute_async(
    #         query=query,
    #         variables=variables,
    #         headers=headers,
    #     )

    #     if not data.get("data"):
    #         raise err.ErrorBase("Unknown Error when running query in IsAttributeUsed")

    #     if isinstance(data["data"].get(field), dict):
    #         return True

    #     elif isinstance(data["data"].get(field), list):
    #         if len(data["data"][field]) == repeated:
    #             return True

    #     raise err.ErrorValidatorIsAttributeUsed(
    #         translate("ERROR_IS_ATTRIBUTE_USED", field, lang=self.lang)
    #     )
