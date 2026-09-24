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

class TicketPriority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

    def __str__(self):
        return self.name.capitalize()

class TicketStatus(Enum):
    OPEN = auto()
    IN_PROGRESS = auto()
    RESOLVED = auto()
    CLOSED = auto()

    def __str__(self):
        return self.name.replace("_", " ").title()