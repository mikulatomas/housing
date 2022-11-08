from typing import Dict, Any
from enum import IntEnum


class OceanProximity(IntEnum):
    less_one_hour = 0
    inland = 1
    near_ocean = 2
    near_bay = 3
    island = 4

    def one_hot(self) -> list[int]:
        """Generates one-hot encoded representation

        Returns:
            list[int]: one-hot encoded value
        """
        values = list(OceanProximity)
        encoding = [0] * len(values)
        encoding[self.value] = 1

        return encoding
    
    @classmethod
    def __modify_schema__(cls, schema: Dict[str, Any]):
        # Human readable IntEnum in fastapi docs
        # source: https://github.com/tiangolo/fastapi/issues/2129
        schema["enum"] = [f"{choice.name} ({choice.value})" for choice in cls]
        return schema

