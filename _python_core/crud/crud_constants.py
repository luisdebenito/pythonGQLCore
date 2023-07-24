from typing import List

CREATE_USER = "createUser"
CREATE_DATE = "createDate"
MODIFIED_USER = "modifiedUser"
MODIFIED_DATE = "modifiedDate"
DELETED_USER = "deletedUser"
DELETED_DATE = "deletedDate"
DEACTIVATE_DATE = "deactivateDate"
NAME = "name"
MINDATE = "minDate"
MAXDATE = "maxDate"
REQUESTDATE = "requestDate"
ACTIVE = "active"

OMIT_FIELDS: List[str] = [
    "_id",
    "id",
    CREATE_USER,
    CREATE_DATE,
    MODIFIED_USER,
    MODIFIED_DATE,
    DELETED_USER,
    DELETED_DATE,
]

CREATE = "Create"
UPDATE = "Update"
DELETE = "Delete"
