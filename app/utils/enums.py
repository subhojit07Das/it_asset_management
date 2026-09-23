from enum import Enum, auto

class AssetType(Enum):
    LAPTOP = auto()
    MONITOR = auto()
    PHONE = auto()

    def __str__(self):
        return self.name.title()

class AssetStatus(Enum):
    AVAILABLE = auto()
    ASSIGNED = auto()
    REPAIR = auto()
    RETIRED = auto()

    def __str__(self):
        return self.name.title()