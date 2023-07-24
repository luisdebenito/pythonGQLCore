from typing import Dict


class GraphqlClientTest:
    async def execute_async(self, **kwargs: Dict) -> Dict:
        return {
            "data": {
                "user": {
                    "id": "14644331-7af8-433b-bfbe-354d9dbfe997",
                    "email": "borja.yanini@.com",
                    "firstName": "Borja",
                    "lastName": "Yanini",
                }
            }
        }


class RabbitMQEventTest:
    async def publish_message(self, *args: Dict) -> None:
        pass


class GQLSourceTest:
    def assemble_data(self, *args: Dict) -> None:
        self.resp_dict = {
            "data": {
                "diary": {
                    "approval": [
                        {
                            "approvedBy": "b23a8219-ff8c-424d-a514-de515158771b",
                            "approvedDate": "2022-05-17T09:09:34.690000Z",
                            "comments": None,
                            "rejectedBy": None,
                            "rejectedDate": None,
                        },
                        {
                            "approvedBy": "1c2dd583-776b-480a-8931-eda36563b447",
                            "approvedDate": "2022-05-18T14:01:48.579000Z",
                            "comments": "",
                            "rejectedBy": None,
                            "rejectedDate": None,
                        },
                    ],
                    "createDate": "2022-05-17T09:09:08.743000Z",
                    "createUser": {"id": "b23a8219-ff8c-424d-a514-de515158771b"},
                    "dateComplete": "2022-05-17T09:09:08.478000Z",
                    "docket": "ggg46901",
                    "events": None,
                    "id": "628366347ea663d4a2cfd0c0",
                    "issues": None,
                    "labourHours": None,
                    "meetings": None,
                    "modifiedDate": "2022-05-18T14:01:57.682000Z",
                    "modifiedUser": {"id": "1c2dd583-776b-480a-8931-eda36563b447"},
                    "plantHours": None,
                    "progressDetails": None,
                    "progressMonitoringDiaryEntries": None,
                    "project": {"id": "65c5351a731a4a4e9edef462c75284a0"},
                    "safetyIssues": None,
                    "shiftDetails": {
                        "date": "2022-05-17T00:00:00.000000Z",
                        "endTime": "11:11",
                        "responsibleEngineer": {
                            "firstName": "Borja",
                            "id": "14644331-7af8-433b-bfbe-354d9dbfe997",
                            "lastName": "Yanini",
                        },
                        "shift": {
                            "id": "621f2d1eebec45518381ec1f",
                            "name": "A  SUPER SUPER  SHIFT",
                            "timecode": {"code": "T23-14", "id": "621dde60c167c954f03121b3"},
                        },
                        "startTime": "09:38",
                    },
                    "subcontractors": None,
                    "timecard": {
                        "activities": [
                            {
                                "activity": None,
                                "detail": {
                                    "eventNumber": None,
                                    "externalDescription": None,
                                    "internalDescription": None,
                                    "isInClientReport": None,
                                    "isReallocateResources": None,
                                    "isRelatedEventExists": None,
                                    "notes": None,
                                },
                                "nonScheduledActivity": {"id": "6182604f33296d942cede2d0"},
                            },
                            {
                                "activity": {"internalId": "BA114480"},
                                "detail": None,
                                "nonScheduledActivity": {"id": None},
                            },
                            {
                                "activity": None,
                                "detail": {
                                    "eventNumber": None,
                                    "externalDescription": None,
                                    "internalDescription": None,
                                    "isInClientReport": None,
                                    "isReallocateResources": None,
                                    "isRelatedEventExists": None,
                                    "notes": None,
                                },
                                "nonScheduledActivity": {"id": "6220af59ad149ce732a8ab92"},
                            },
                        ],
                        "resourceActivities": [
                            {
                                "resource": {
                                    "active": True,
                                    "autoDocket": None,
                                    "class": {
                                        "id": "617fec8406cb035fa0eab8d7",
                                        "name": "Internal " "Labour",
                                        "type": {"name": "Internal " "Labour"},
                                        "workforceGroup": None,
                                    },
                                    "company": {
                                        "id": "617fe244d0e75a6bb27acdf9",
                                        "name": "HOCHTIEF " "Infrastructure " "GmbH " "Dusseldorf",
                                    },
                                    "employeeNumber": "",
                                    "id": "620cec77921c8f71074d5ac3",
                                    "jdeNumber": None,
                                    "middleName": "P",
                                    "name": "Juan",
                                    "resourceTitle": {
                                        "id": "617fe11f912804b6edc42686",
                                        "name": "Baufuehrer",
                                    },
                                    "startDate": "44501",
                                    "surname": "Pachanga",
                                    "terminateDate": None,
                                    "type": {
                                        "id": "617fec0e912804b6edc42689",
                                        "name": "Internal " "Labour",
                                    },
                                },
                                "workingActivities": [
                                    {
                                        "activity": None,
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 0.5,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": "6182604f33296d942cede2d0",
                                            "name": "I " "am " "Additional " "Work",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "ADDITIONAL_WORK",
                                        },
                                    },
                                    {
                                        "activity": {
                                            "internalId": "BA114480",
                                            "name": "1. "
                                            "Ankerlage "
                                            "Bohrpfahlwand "
                                            "Verbau "
                                            "Nr. "
                                            "18",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "FIXED_DURATION",
                                        },
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 0.5,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": None,
                                            "name": None,
                                            "projectId": None,
                                            "type": None,
                                        },
                                    },
                                    {
                                        "activity": None,
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 1,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": "6220af59ad149ce732a8ab92",
                                            "name": "dddd",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "OBSTACLE",
                                        },
                                    },
                                ],
                            },
                            {
                                "resource": {
                                    "active": True,
                                    "autoDocket": None,
                                    "class": {
                                        "id": "6272816f32d7cea97244c47e",
                                        "name": "RC " "Developers",
                                        "type": {"name": "Developers"},
                                        "workforceGroup": None,
                                    },
                                    "company": {
                                        "id": "617fe244d0e75a6bb27acdf9",
                                        "name": "HOCHTIEF " "Infrastructure " "GmbH " "Dusseldorf",
                                    },
                                    "employeeNumber": None,
                                    "id": "627281c932d7cea97244c482",
                                    "jdeNumber": None,
                                    "middleName": "",
                                    "name": "IL " "JCN",
                                    "resourceTitle": None,
                                    "startDate": "2022-05-04T00:00:00.000000Z",
                                    "surname": "test",
                                    "terminateDate": None,
                                    "type": {
                                        "id": "627280ff32d7cea97244c478",
                                        "name": "Developers",
                                    },
                                },
                                "workingActivities": [
                                    {
                                        "activity": None,
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 0.5,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": "6182604f33296d942cede2d0",
                                            "name": "I " "am " "Additional " "Work",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "ADDITIONAL_WORK",
                                        },
                                    },
                                    {
                                        "activity": {
                                            "internalId": "BA114480",
                                            "name": "1. "
                                            "Ankerlage "
                                            "Bohrpfahlwand "
                                            "Verbau "
                                            "Nr. "
                                            "18",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "FIXED_DURATION",
                                        },
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 0.5,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": None,
                                            "name": None,
                                            "projectId": None,
                                            "type": None,
                                        },
                                    },
                                    {
                                        "activity": None,
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 1,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": "6220af59ad149ce732a8ab92",
                                            "name": "dddd",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "OBSTACLE",
                                        },
                                    },
                                ],
                            },
                            {
                                "resource": {
                                    "active": None,
                                    "autoDocket": None,
                                    "class": {
                                        "id": "617feef706cb035fa0eab8e7",
                                        "name": "Subcontractor",
                                        "type": {"name": "Crews"},
                                        "workforceGroup": None,
                                    },
                                    "company": {
                                        "id": "617fe244d0e75a6bb27acdf9",
                                        "name": "HOCHTIEF " "Infrastructure " "GmbH " "Dusseldorf",
                                    },
                                    "employeeNumber": None,
                                    "id": "6272516832d7cea97244c465",
                                    "jdeNumber": None,
                                    "middleName": None,
                                    "name": "Assembler " "T " "Hochtief " "NEW",
                                    "resourceTitle": None,
                                    "startDate": "2022-05-05T09:45:35.321000Z",
                                    "surname": None,
                                    "terminateDate": None,
                                    "type": None,
                                },
                                "workingActivities": [
                                    {
                                        "activity": None,
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 0.5,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": "6182604f33296d942cede2d0",
                                            "name": "I " "am " "Additional " "Work",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "ADDITIONAL_WORK",
                                        },
                                    },
                                    {
                                        "activity": {
                                            "internalId": "BA114480",
                                            "name": "1. "
                                            "Ankerlage "
                                            "Bohrpfahlwand "
                                            "Verbau "
                                            "Nr. "
                                            "18",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "FIXED_DURATION",
                                        },
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 0.5,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": None,
                                            "name": None,
                                            "projectId": None,
                                            "type": None,
                                        },
                                    },
                                    {
                                        "activity": None,
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 1,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": "6220af59ad149ce732a8ab92",
                                            "name": "dddd",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "OBSTACLE",
                                        },
                                    },
                                ],
                            },
                            {
                                "resource": {
                                    "active": None,
                                    "autoDocket": None,
                                    "class": {
                                        "id": "617feef706cb035fa0eab8e7",
                                        "name": "Subcontractor",
                                        "type": {"name": "Crews"},
                                        "workforceGroup": None,
                                    },
                                    "company": {
                                        "id": "617fe244d0e75a6bb27acdf9",
                                        "name": "HOCHTIEF " "Infrastructure " "GmbH " "Dusseldorf",
                                    },
                                    "employeeNumber": None,
                                    "id": "627252d332d7cea97244c467",
                                    "jdeNumber": None,
                                    "middleName": None,
                                    "name": "Elektriker " "hoch",
                                    "resourceTitle": None,
                                    "startDate": "2022-05-04T10:17:22.296000Z",
                                    "surname": None,
                                    "terminateDate": None,
                                    "type": None,
                                },
                                "workingActivities": [
                                    {
                                        "activity": None,
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 0.5,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": "6182604f33296d942cede2d0",
                                            "name": "I " "am " "Additional " "Work",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "ADDITIONAL_WORK",
                                        },
                                    },
                                    {
                                        "activity": {
                                            "internalId": "BA114480",
                                            "name": "1. "
                                            "Ankerlage "
                                            "Bohrpfahlwand "
                                            "Verbau "
                                            "Nr. "
                                            "18",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "FIXED_DURATION",
                                        },
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 0.5,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": None,
                                            "name": None,
                                            "projectId": None,
                                            "type": None,
                                        },
                                    },
                                    {
                                        "activity": None,
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 1,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": "6220af59ad149ce732a8ab92",
                                            "name": "dddd",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "OBSTACLE",
                                        },
                                    },
                                ],
                            },
                            {
                                "resource": {
                                    "active": None,
                                    "autoDocket": True,
                                    "class": {
                                        "id": "617feef706cb035fa0eab8e7",
                                        "name": "Subcontractor",
                                        "type": {"name": "Crews"},
                                        "workforceGroup": None,
                                    },
                                    "company": {
                                        "id": "617fe251d0e75a6bb27acdfa",
                                        "name": "Hilti " "& " "Associates",
                                    },
                                    "employeeNumber": None,
                                    "id": "62502a5aaa9f10e66c1812c0",
                                    "jdeNumber": None,
                                    "middleName": None,
                                    "name": "EQUIPMENT " "TEST",
                                    "resourceTitle": None,
                                    "startDate": None,
                                    "surname": None,
                                    "terminateDate": None,
                                    "type": {
                                        "id": "617fec2b912804b6edc4268c",
                                        "name": "Leased " "Equipment",
                                    },
                                },
                                "workingActivities": [
                                    {
                                        "activity": None,
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 0.5,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": "6182604f33296d942cede2d0",
                                            "name": "I " "am " "Additional " "Work",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "ADDITIONAL_WORK",
                                        },
                                    },
                                    {
                                        "activity": {
                                            "internalId": "BA114480",
                                            "name": "1. "
                                            "Ankerlage "
                                            "Bohrpfahlwand "
                                            "Verbau "
                                            "Nr. "
                                            "18",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "FIXED_DURATION",
                                        },
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 0.5,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": None,
                                            "name": None,
                                            "projectId": None,
                                            "type": None,
                                        },
                                    },
                                    {
                                        "activity": None,
                                        "activityTime": {
                                            "doubleTime": 0,
                                            "hoursWorked": None,
                                            "numberOfWorkers": None,
                                            "overtime": 0,
                                            "regular": 1,
                                            "unitOfMeasure": None,
                                        },
                                        "nonScheduledActivity": {
                                            "id": "6220af59ad149ce732a8ab92",
                                            "name": "dddd",
                                            "projectId": "65c5351a731a4a4e9edef462c75284a0",
                                            "type": "OBSTACLE",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                    "verbalInstructions": {"comments": ""},
                }
            }
        }

    def get_data(self) -> Dict:
        return self.resp_dict
