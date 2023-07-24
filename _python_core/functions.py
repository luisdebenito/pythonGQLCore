import hashlib
import re
from typing import Any, Dict, List, Tuple, Union

from bson import ObjectId
from _python_core.constants import ID, _ID


def getHash(item: Any) -> str:
    return hashlib.sha256(str(item).encode("utf-8")).hexdigest()


def isValidObjectId(my_string: str) -> bool:
    return ObjectId.is_valid(my_string)


def getId(entry: Dict) -> Union[ObjectId, str]:
    if "_id" in entry.keys():
        return entry["_id"]
    elif "id" in entry.keys():
        return entry["id"]
    else:
        return ""


def isValidID(entry: Dict) -> bool:
    entry_id = getId(entry)

    if bool(entry_id):
        if isinstance(entry_id, str):
            return isValidObjectId(entry_id)
        elif isinstance(entry_id, ObjectId):
            return isValidObjectId(str(entry_id))

    return False


def entryHasIDNoNull(entry: Dict) -> bool:
    return bool(entry.get("id")) or bool(entry.get("_id"))


def find_type_in_schema(className: str, file: str, field: str) -> str | None:
    # sourcery skip: move-assign

    REGEX = r"type\s" + re.escape(className) + r"\s(.*?)}"
    REGEX2 = re.escape(field) + r":\s(\w*)"
    DICT2TYPES = {"String": "str", "Boolean": "bool", "Float": "float", "Int": "int"}

    with open(file, "r") as schema:
        schemaToString = schema.read().replace("\n", "")

    if (
        re.search(REGEX, schemaToString)
        and (_match := re.search(REGEX, schemaToString))
        and (filtered_text := _match[0])
        and re.search(REGEX2, filtered_text)
    ):
        typeField = re.search(REGEX2, filtered_text)[1]  # type: ignore
        return DICT2TYPES.get(typeField)

    return None


def get_ids_from_schemas(schemas: List[Dict]) -> List:
    schemasFiltered: List[Dict] = list(
        filter(lambda schema: (schema.get(_ID, schema.get(ID))), schemas)
    )
    return [str(schema.get(ID, schema.get(_ID))) for schema in schemasFiltered]


def is_schema_in_data_provided(validSchemas: List[Any], entity: Any) -> bool:
    ids = [str(schema.get(_ID)) for schema in validSchemas]
    return str(entity.schema.get(_ID, "")) in ids


def get_entries_in_validSchemas(fields: List[str], validSchemas: List[Dict]) -> List[Any]:
    return list(
        filter(
            lambda schema: contains_all_fields(schema, fields),
            validSchemas,
        )
    )


def contains_all_fields(schema: Dict, fields: List[str]) -> bool:
    return all(field in schema for field in fields)


def transform_list_dict_to_list_tuple(dict: List[Dict]) -> List[tuple]:
    tupleRes: List[Tuple] = []
    if len(dict):
        keys = list(dict[0].keys())
        values = list(dict[0].values())
        tupleList = list(values)
        tupleList[0] = 1 if tupleList[0] == "asc" else -1
        tupleVals = tuple([keys[0], tupleList[0]])
        tupleRes = [tupleVals]
    return tupleRes
