import os
from typing import Generator, Union

import pymongo
import mongomock
import pytest

MONGODB_PROTOCOL = "mongodb://"
MONGODB_USERNAME = ""
MONGODB_PASSWORD = ""
MONGODB_HOSTNAME = "localhost:27017"

mongo_connection_string = MONGODB_PROTOCOL + MONGODB_HOSTNAME
if MONGODB_USERNAME and MONGODB_PASSWORD:
    mongo_connection_string = (
        MONGODB_PROTOCOL + MONGODB_USERNAME + ":" + MONGODB_PASSWORD + "@" + MONGODB_HOSTNAME
    )

os.environ["MOCK_TEST"] = "True"
os.environ["PYTHON_DEBUG_TEST"] = "Y"  # DO NOT CHANGE THIS VARIABLE EVER
MOCK_TEST = os.getenv("MOCK_TEST") == "True"

mongo: Union[pymongo.MongoClient, mongomock.MongoClient] = (
    mongomock.MongoClient() if MOCK_TEST else pymongo.MongoClient(mongo_connection_string)
)

db = "test"
mongo_db = mongo[db]
mongo_col = mongo_db["crud"]


def clean_ddbb() -> None:
    mongo_db.drop_collection("test")
    mongo_db.drop_collection("mock")
    mongo_db.drop_collection("crud")
    mongo_db.drop_collection("changeLog")


clean_ddbb()


@pytest.fixture(scope="session", autouse=False)
def my_mongos() -> Union[Generator, None]:
    yield mongo, db
    mongo.drop_database(db)
    mongo.close()
