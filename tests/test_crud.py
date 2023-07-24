# import os
# import sys
# from typing import List

# import pytest
# from bson import ObjectId

# CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

# from _python_core import crud

# # Kurt USERID
# USER = "02477c69-56f4-4e77-921a-23a2a82a335e"
# PROJECT_ID = "12070c789f30472094bbcf61923ecab4"


# class Collection:
#     CRUD = "crud"
#     CHANGELOG = "changeLog"


# class TestCRUD_Insert:
# #     async def test_insert_one_with_id(self, my_mongos: List) -> None:
#         entry = {
#             "_id": ObjectId("61016f14696cd95e1764b120"),
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         msg, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )
#         changelogList = await crud.get(
#             my_mongos[2]["changeLog"], **{"parentID": "61016f14696cd95e1764b120"}
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "has successfully been inserted" in msg[0]

#         # entry
#         assert entry is not None
#         assert isinstance(entry, list)
#         assert len(entry) == 1
#         assert str(entry[0]["_id"]) == "61016f14696cd95e1764b120"
#         assert entry[0]["one"] == 1
#         assert "createDate" in entry[0].keys()
#         assert "createUser" in entry[0].keys()
#         assert entry[0]["createUser"] == {"id": USER}
#         assert "modifiedDate" not in entry[0].keys()
#         assert "modifiedUser" not in entry[0].keys()
#         assert "deletedDate" not in entry[0].keys()
#         assert "deletedUser" not in entry[0].keys()

#         # changeLog
#         assert len(changelogList) == 1
#         changelog = changelogList[0]
#         assert bool(changelog)
#         assert "changeLog" in changelog.keys()
#         assert bool(changelog["changeLog"]) is False
#         assert "collection" in changelog.keys()
#         assert bool(changelog["collection"])
#         assert "createDate" in changelog.keys()
#         assert bool(changelog["createDate"])
#         assert "createUser" in changelog.keys()
#         assert bool(changelog["createUser"])
#         assert "action" in changelog.keys()
#         assert changelog["action"] == "Create"

# #     async def test_insert_one_with_id_null(self, my_mongos: List) -> None:
#         """Insert One with ID"""
#         entry = {
#             "_id": None,
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         msg, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "has successfully been inserted" in msg[0]

#         # entry
#         assert entry is not None
#         assert isinstance(entry, list)
#         assert len(entry) == 1
#         assert entry[0]["one"] == 1
#         assert "createDate" in entry[0].keys()
#         assert "createUser" in entry[0].keys()
#         assert entry[0]["createUser"] == {"id": USER}
#         assert "modifiedDate" not in entry[0].keys()
#         assert "modifiedUser" not in entry[0].keys()
#         assert "deletedDate" not in entry[0].keys()
#         assert "deletedUser" not in entry[0].keys()

# #     async def test_insert_one_with_id_empty_string(self, my_mongos: List) -> None:
#         """Insert One with ID"""
#         entry = {
#             "_id": "",
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         msg, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "has successfully been inserted" in msg[0]

#         # entry
#         assert entry is not None
#         assert isinstance(entry, list)
#         assert len(entry) == 1
#         assert entry[0]["one"] == 1
#         assert "createDate" in entry[0].keys()
#         assert "createUser" in entry[0].keys()
#         assert entry[0]["createUser"] == {"id": USER}
#         assert "modifiedDate" not in entry[0].keys()
#         assert "modifiedUser" not in entry[0].keys()
#         assert "deletedDate" not in entry[0].keys()
#         assert "deletedUser" not in entry[0].keys()

# #     async def test_insert_one_with_id_empty_string_2(self, my_mongos: List) -> None:
#         """Insert One with ID"""
#         entry = {
#             "id": "",
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         msg, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "has successfully been inserted" in msg[0]

#         # entry
#         assert entry is not None
#         assert isinstance(entry, list)
#         assert len(entry) == 1
#         assert entry[0]["one"] == 1
#         assert "createDate" in entry[0].keys()
#         assert "createUser" in entry[0].keys()
#         assert entry[0]["createUser"] == {"id": USER}
#         assert "modifiedDate" not in entry[0].keys()
#         assert "modifiedUser" not in entry[0].keys()
#         assert "deletedDate" not in entry[0].keys()
#         assert "deletedUser" not in entry[0].keys()

# #     async def test_insert_one_with_id_null_2(self, my_mongos: List) -> None:
#         """Insert One with ID"""
#         entry = {
#             "id": None,
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         msg, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "has successfully been inserted" in msg[0]

#         # entry
#         assert entry is not None
#         assert isinstance(entry, list)
#         assert len(entry) == 1
#         assert entry[0]["one"] == 1
#         assert "createDate" in entry[0].keys()
#         assert "createUser" in entry[0].keys()
#         assert entry[0]["createUser"] == {"id": USER}
#         assert "modifiedDate" not in entry[0].keys()
#         assert "modifiedUser" not in entry[0].keys()
#         assert "deletedDate" not in entry[0].keys()
#         assert "deletedUser" not in entry[0].keys()

# #     async def test_insert_one_with_id_2(self, my_mongos: List) -> None:
#         """Insert One with ID"""
#         entry = {
#             "id": ObjectId("616c29835104555d364a6186"),
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         msg, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "has successfully been inserted" in msg[0]

# #     async def test_insert_one_with_id_wrong(self, my_mongos: List) -> None:
#         """Insert One with ID"""
#         entry = {
#             "id": "616c29835104555d364a618",
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         msg, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "This entry has a wrong id" in msg[0]

# #     async def test_insert_one_without_id(self, my_mongos: List) -> None:
#         """Insert One without ID"""
#         entry = {"one": 1}
#         msg, returned_entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         changelogList = await crud.get(
#             my_mongos[2]["changeLog"], **{"parentID": str(returned_entry[0]["_id"])}
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "has successfully been inserted" in msg[0]

#         # entry
#         assert returned_entry is not None
#         assert isinstance(returned_entry, list)
#         assert len(returned_entry) == 1
#         assert returned_entry[0]["one"] == 1
#         assert "createDate" in returned_entry[0].keys()
#         assert "createUser" in returned_entry[0].keys()
#         assert returned_entry[0]["createUser"] == {"id": USER}
#         assert "modifiedDate" not in returned_entry[0].keys()
#         assert "modifiedUser" not in returned_entry[0].keys()
#         assert "deletedDate" not in returned_entry[0].keys()
#         assert "deletedUser" not in returned_entry[0].keys()

#         # changeLog
#         assert len(changelogList) == 1
#         changelog = changelogList[0]
#         assert bool(changelog)
#         assert "changeLog" in changelog.keys()
#         assert bool(changelog["changeLog"]) is False
#         assert "collection" in changelog.keys()
#         assert bool(changelog["collection"])
#         assert "createDate" in changelog.keys()
#         assert bool(changelog["createDate"])
#         assert "createUser" in changelog.keys()
#         assert bool(changelog["createUser"])
#         assert "action" in changelog.keys()
#         assert changelog["action"] == "Create"

# #     async def test_insert_many(self, my_mongos: List) -> None:
#         """Insert or Update Many"""
#         entries = [
#             {"_id": ObjectId("61016f14696cd95e1764b122"), "one": 1},
#             {"_id": ObjectId("61016f14696cd95e1764b132"), "two": 2},
#             {"_id": ObjectId("61016f14696cd95e1764b142"), "two": 2},
#             {"three": 3},
#         ]
#         msg, entries = await crud.insert_or_update_many(
#             entries, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 4
#         for i in msg:
#             assert isinstance(i, str)

#         # data
#         assert isinstance(entries, list)
#         assert len(entries) == 4
#         _is_ok = False
#         for i in entries:
#             if str(i["_id"]) == "61016f14696cd95e1764b122":
#                 _is_ok = True
#                 assert isinstance(i, dict)
#                 assert i is not None
#                 assert i["one"] == 1
#                 assert "createDate" in i.keys()
#                 assert "createUser" in i.keys()
#                 assert i["createUser"] == {"id": USER}
#                 assert "modifiedDate" not in i.keys()
#                 assert "modifiedUser" not in i.keys()
#                 assert "deletedDate" not in i.keys()
#                 assert "deletedUser" not in i.keys()
#         assert _is_ok

# #     async def test_insert_many_empty_entry(self, my_mongos: List) -> None:
#         msg, entry = await crud.insert_or_update_many(
#             [{}], PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         assert bool(msg)
#         assert bool(entry)
#         assert msg[0] == "Entry is empty. Nothing to insert"
#         assert bool(entry[0]) is False

# #     async def test_insert_one_empty_entry(self, my_mongos: List) -> None:
#         msg, entry = await crud.insert_or_update_one(
#             {}, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         assert bool(msg)
#         assert bool(entry)
#         assert msg[0] == "Entry is empty. Nothing to insert"
#         assert bool(entry[0]) is False


# class TestCRUD_Update:
# #     async def test_update_one_with_ID(self, my_mongos: List) -> None:
#         """Modify Existing One with _id"""

#         # insert
#         entry = {
#             "_id": ObjectId("61016f14696cd95e1764b121"),
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         msg, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # update
#         entry = {"_id": ObjectId("61016f14696cd95e1764b121"), "one": 3}
#         msg, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # changelog
#         filter = {"parentID": "61016f14696cd95e1764b121", "action": "Update"}
#         changelogEntry = await crud.get(my_mongos[2][Collection.CHANGELOG], **filter)

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "has successfully been updated" in msg[0]

#         # entry
#         assert entry is not None
#         assert isinstance(entry, list)
#         assert len(entry) == 1
#         assert str(entry[0]["_id"]) == "61016f14696cd95e1764b121"
#         assert entry[0]["one"] == 3
#         assert entry[0]["projectId"] == PROJECT_ID
#         assert "createDate" in entry[0].keys()
#         assert "createUser" in entry[0].keys()
#         assert entry[0]["createUser"] == {"id": USER}
#         assert "modifiedDate" in entry[0].keys()
#         assert "modifiedUser" in entry[0].keys()
#         assert entry[0]["modifiedUser"] == {"id": USER}
#         assert "deletedDate" not in entry[0].keys()
#         assert "deletedUser" not in entry[0].keys()

#         # Changelog
#         assert changelogEntry is not None
#         assert isinstance(changelogEntry, list)
#         assert len(changelogEntry) == 1
#         assert changelogEntry[0]["parentID"] == "61016f14696cd95e1764b121"
#         assert changelogEntry[0]["action"] == "Update"
#         assert len(changelogEntry[0]["changeLog"]) == 1
#         assert "createDate" in changelogEntry[0].keys()
#         assert "createUser" in changelogEntry[0].keys()
#         assert changelogEntry[0]["createUser"] == {"id": USER}
#         assert "collection" in changelogEntry[0].keys()
#         assert "modifiedDate" not in changelogEntry[0].keys()
#         assert "modifiedUser" not in changelogEntry[0].keys()
#         assert "deletedDate" not in changelogEntry[0].keys()
#         assert "deletedUser" not in changelogEntry[0].keys()

# #     async def test_omit_fields_update_one(self, my_mongos: List) -> None:
#         """Check if deleted entry is not returned"""
#         omit_fields = ["two"]
#         entries = {"_id": ObjectId("61016f14696cd95e1764b142"), "two": 30}
#         _, entries = await crud.insert_or_update_one(
#             entries,
#             PROJECT_ID,
#             USER,
#             my_mongos[2],
#             Collection.CRUD,
#             omitFields=omit_fields,
#         )

#         assert len(entries) == 1

#         filter = {"parentID": "61016f14696cd95e1764b142"}
#         entry = await crud.get_with_limit(my_mongos[2][Collection.CHANGELOG], 1, **filter)

#         assert len(entry) == 1
#         assert entry[0]["action"] == "Create"

# #     async def test_omit_fields_update_many(self, my_mongos: List) -> None:
#         """Check if deleted entry is not returned"""
#         omit_fields = ["two"]
#         entries = [
#             {"_id": ObjectId("61016f14696cd95e1764b142"), "two": 20},
#         ]
#         _, entries = await crud.insert_or_update_many(
#             entries,
#             PROJECT_ID,
#             USER,
#             my_mongos[2],
#             Collection.CRUD,
#             omitFields=omit_fields,
#         )

#         assert len(entries) == 1

#         filter = {"parentID": "61016f14696cd95e1764b142"}
#         entry = await crud.get_with_limit(my_mongos[2][Collection.CHANGELOG], 1, **filter)

#         assert len(entry) == 1
#         assert entry[0]["action"] == "Create"

# #     async def test_update_one_with_no_changes(self, my_mongos: List) -> None:
#         """Check if when updating and entry with no changes, no auditFields are updated"""

#         entries = {"_id": ObjectId("61016f14696cd95e1764b182"), "two": 30}
#         _, entries = await crud.insert_or_update_one(
#             entries,
#             PROJECT_ID,
#             USER,
#             my_mongos[2],
#             Collection.CRUD,
#         )

#         entries = {"_id": ObjectId("61016f14696cd95e1764b182"), "two": 30}
#         msg, entry = await crud.insert_or_update_one(
#             entries,
#             PROJECT_ID,
#             USER,
#             my_mongos[2],
#             Collection.CRUD,
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "This entry has not changed" in msg[0]

#         # entry
#         assert entry is not None
#         assert isinstance(entry, list)
#         assert len(entry) == 1
#         assert str(entry[0]["_id"]) == "61016f14696cd95e1764b182"
#         assert entry[0]["two"] == 30
#         assert entry[0]["projectId"] == PROJECT_ID
#         assert "createDate" in entry[0].keys()
#         assert "createUser" in entry[0].keys()
#         assert entry[0]["createUser"] == {"id": USER}
#         assert "modifiedDate" not in entry[0].keys()
#         assert "modifiedUser" not in entry[0].keys()
#         assert "deletedDate" not in entry[0].keys()
#         assert "deletedUser" not in entry[0].keys()


# class TestCRUD_Read:
# #     async def test_get_with_limit(self, my_mongos: List) -> None:
#         """Check if deleted entry is not returned"""

#         # insert
#         entry = {
#             "_id": ObjectId("61016f14696cd95e1764b122"),
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         _, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # update 1
#         entry = {"_id": ObjectId("61016f14696cd95e1764b122"), "one": 3}
#         _, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # update 2
#         entry = {"_id": ObjectId("61016f14696cd95e1764b122"), "one": 5}
#         _, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # changelog
#         filter = {"parentID": "61016f14696cd95e1764b122"}
#         entry = await crud.get_with_limit(my_mongos[2][Collection.CHANGELOG], 1, **filter)

#         # entry
#         assert entry is not None
#         assert isinstance(entry, list)
#         assert len(entry) == 1
#         assert entry[0]["parentID"] == "61016f14696cd95e1764b122"

# #     async def test_get_single(self, my_mongos: List) -> None:
#         """Check if deleted entry is not returned"""

#         # insert
#         entry = {
#             "_id": ObjectId("61016f14696cd95e1764b102"),
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         _, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # get
#         filter = {"_id": ObjectId("61016f14696cd95e1764b102")}
#         entry = await crud.get_single(my_mongos[2][Collection.CRUD], **filter)

#         # entry
#         assert entry is not None
#         assert isinstance(entry, dict)
#         assert str(entry["_id"]) == "61016f14696cd95e1764b102"


# class TestCRUD_HardDelete:
# #     async def test_hard_delete_one(self, my_mongos: List) -> None:
#         """Delete Hard one"""

#         # insert
#         entry = {
#             "_id": ObjectId("61016f14696cd95e1764b122"),
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         _, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # delete
#         msg, entry = await crud.delete_one(
#             my_mongos[2], Collection.CRUD, "61016f14696cd95e1764b122"
#         )

#         # get after delete
#         entryAfterDelete = await crud.get_by_id(
#             my_mongos[2][Collection.CHANGELOG], "61016f14696cd95e1764b122"
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "Successfully deleted" in msg[0]

#         # entry After Delete
#         assert bool(entryAfterDelete) is False

# #     async def test_hard_delete_many(self, my_mongos: List) -> None:
#         """Delete Hard one"""

#         # insert
#         data = [
#             {
#                 "_id": ObjectId("61016f14696cd95e1764b122"),
#             },
#             {
#                 "_id": ObjectId("61016f14696cd95e1764b142"),
#             },
#             {
#                 "_id": ObjectId("61016f14696cd95e1764b162"),
#             },
#         ]
#         _, entries = await crud.insert_or_update_many(
#             data, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # delete
#         msg, deletedEntries = await crud.delete_many(
#             my_mongos[2],
#             Collection.CRUD,
#             [
#                 "61016f14696cd95e1764b122",
#                 "61016f14696cd95e1764b142",
#                 "61016f14696cd95e1764b162",
#             ],
#         )

#         # get after delete
#         filter = {
#             "$or": [
#                 {"_id": ObjectId("61016f14696cd95e1764b122")},
#                 {"_id": ObjectId("61016f14696cd95e1764b142")},
#                 {"_id": ObjectId("61016f14696cd95e1764b162")},
#             ]
#         }
#         entryAfterDelete = await crud.get(my_mongos[2][Collection.CRUD], **filter)

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 3
#         for message in msg:
#             assert isinstance(message, str)
#             assert "Successfully deleted" in message

#         # deleted entries
#         assert deletedEntries is not None
#         assert isinstance(deletedEntries, list)
#         assert len(deletedEntries) == 3

#         # entry After Delete
#         assert entryAfterDelete is not None
#         assert isinstance(entryAfterDelete, list)
#         assert len(entryAfterDelete) == 0


# class TestCRUD_SoftDelete:
# #     async def test_soft_delete_one(self, my_mongos: List) -> None:
#         """Delete Soft one"""

#         # insert
#         entry = {
#             "_id": ObjectId("61016f14696cd95e1764b122"),
#             "one": 1,
#             "projectId": PROJECT_ID,
#         }
#         _, entry = await crud.insert_or_update_one(
#             entry, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # delete
#         msg, entry = await crud.delete_soft_one(
#             my_mongos[2],
#             Collection.CRUD,
#             "61016f14696cd95e1764b122",
#             PROJECT_ID,
#             USER,
#         )

#         # changelog
#         filter = {"parentID": "61016f14696cd95e1764b122", "action": "Delete"}
#         changelogEntry = await crud.get(my_mongos[2][Collection.CHANGELOG], **filter)

#         # get after delete
#         entryAfterDelete = await crud.get_by_id(
#             my_mongos[2][Collection.CHANGELOG], "61016f14696cd95e1764b122"
#         )

#         # msg
#         assert msg is not None
#         assert isinstance(msg, list)
#         assert len(msg) == 1
#         assert isinstance(msg[0], str)
#         assert "has successfully been soft deleted" in msg[0]

#         # entry
#         assert entry is not None
#         assert isinstance(entry, list)
#         assert len(entry) == 1
#         assert str(entry[0]["_id"]) == "61016f14696cd95e1764b122"
#         assert entry[0]["one"] == 1
#         assert "createDate" in entry[0].keys()
#         assert "createUser" in entry[0].keys()
#         assert entry[0]["createUser"] == {"id": USER}
#         assert "modifiedDate" not in entry[0].keys()
#         assert "modifiedUser" not in entry[0].keys()
#         assert "deletedDate" in entry[0].keys()
#         assert "deletedUser" in entry[0].keys()
#         assert entry[0]["deletedUser"] == {"id": USER}
#         assert entry[0]["deletedDate"] >= entry[0]["createDate"]

#         # changelog
#         assert changelogEntry is not None
#         assert isinstance(changelogEntry, list)
#         assert len(changelogEntry) == 1
#         assert changelogEntry[0]["parentID"] == "61016f14696cd95e1764b122"
#         assert changelogEntry[0]["action"] == "Delete"
#         assert len(changelogEntry[0]["changeLog"]) == 0
#         assert "createDate" in changelogEntry[0].keys()
#         assert "createUser" in changelogEntry[0].keys()
#         assert changelogEntry[0]["createUser"] == {"id": USER}
#         assert "modifiedDate" not in changelogEntry[0].keys()
#         assert "modifiedUser" not in changelogEntry[0].keys()
#         assert "deletedDate" not in changelogEntry[0].keys()
#         assert "deletedUser" not in changelogEntry[0].keys()

#         # entry After Delete
#         assert bool(entryAfterDelete) is False

# #     async def test_soft_delete_many(self, my_mongos: List) -> None:
#         """Delete Soft Many"""

#         # insert
#         entries = [
#             {"_id": ObjectId("61016f14696cd95e1764b123"), "one": 1},
#             {"_id": ObjectId("61016f14696cd95e1764b133"), "two": 2},
#             {"_id": ObjectId("61016f14696cd95e1764b143"), "two": 2},
#             {"three": 3},
#         ]
#         _, entries = await crud.insert_or_update_many(
#             entries, PROJECT_ID, USER, my_mongos[2], Collection.CRUD
#         )

#         # delete
#         messageDeleted, entriesDeleted = await crud.delete_soft_many(
#             my_mongos[2],
#             Collection.CRUD,
#             [
#                 "61016f14696cd95e1764b123",
#                 "61016f14696cd95e1764b133",
#                 "61016f14696cd95e1764b143",
#             ],
#             PROJECT_ID,
#             USER,
#         )

#         # msg
#         assert messageDeleted is not None
#         assert isinstance(messageDeleted, list)
#         assert len(messageDeleted) == 3
#         for message in messageDeleted:
#             assert isinstance(message, str)
#             assert "has successfully been soft deleted" in message

#         # entry
#         assert entriesDeleted is not None
#         assert len(entriesDeleted) == 3
#         assert isinstance(entriesDeleted, list)
#         for entry in entriesDeleted:
#             assert isinstance(entry, dict)
#             assert "projectId" in entry.keys()
#             assert "createDate" in entry.keys()
#             assert "createUser" in entry.keys()
#             assert entry["createUser"] == {"id": USER}
#             assert "modifiedDate" not in entry.keys()
#             assert "modifiedUser" not in entry.keys()
#             assert "deletedDate" in entry.keys()
#             assert "deletedUser" in entry.keys()
#             assert entry["deletedUser"] == {"id": USER}
#             assert entry["deletedDate"] >= entry["createDate"]
