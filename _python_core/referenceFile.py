from typing import Any, Dict, List, TypeVar

from _python_core.BaseClass import BaseOne

ReferenceFileObject = TypeVar("ReferenceFileObject", bound="ReferenceFile")

# Type Defined in the GQL Schema
TReferenceFile = Dict[str, Any]


class ReferenceFileBase:
    collection: str = "files"


class ReferenceFile(ReferenceFileBase, BaseOne):
    def __init__(self, **kwargs: Any):
        BaseOne.__init__(self, **kwargs)

    # Overrides abstract method
    async def validate_to_insertUpdate(
        self, idx: int = 0, validSchemas: List[TReferenceFile] = []
    ) -> bool:
        self.index = idx
        self.reset_errors()
        # Add here all the business rules
        return all(
            [
                True,
            ]
        )

    # Overrides abstract method
    async def validate_to_delete(self, validSchemas: List[TReferenceFile] = []) -> bool:
        self.reset_errors()

        # Add here all the business rules
        return all(
            [
                True,
            ]
        )
