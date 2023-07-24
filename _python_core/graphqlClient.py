import os
import sys

from python_graphql_client import GraphqlClient

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))
import _python_core.Mock as mock

GRAPHQL_FEDERATION_URL_LOCALHOST = "http://localhost:4000/graphql"


class IGraphqlClient:
    def __init__(self, endpoint: str = GRAPHQL_FEDERATION_URL_LOCALHOST) -> None:
        self.graphql_client = (
            mock.GraphqlClientTest()
            if os.getenv("PYTHON_DEBUG_TEST")
            else GraphqlClient(endpoint=endpoint)
        )
