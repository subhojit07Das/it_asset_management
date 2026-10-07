from app.utils.enums import AssetStatus, AssetType, TicketPriority, TicketStatus

def get_valid_id(prompt="Enter ID: "):
    while True:
        value = input(prompt)
        
        if not value.isdigit():
            print(f"Please enter a valid number. You typed: {value}")
            continue

        else:
            break
        
    return int(value)

def get_valid_text(prompt, allow_cancel=True):
    while True:
        value = input(prompt).strip()

        if allow_cancel and value.lower() == "c":
            print("Cancelled.")
            return None

        if value == "":
            print("This field cannot be empty. Please try again.")
            continue

        return value

def get_valid_name(prompt):
    while True:
        value = input(prompt).strip()

        if value.lower() == "c":
            print("Cancelled.")
            return None
        
        if value == "":
            print("This field cannot be empty. Please try again.")
            continue

        name = " ".join(value.split()).upper()
        return name

def get_valid_asset_type(prompt):
    while True:
        value = input(prompt)

        if value.lower() == "c":
            print("Cancelled.")
            return None
        
        elif value == "":
            print("This field cannot be empty. Please try again.")
            continue

        elif value == "LAPTOP" or value == "laptop":
            return AssetType.LAPTOP

        elif value == "PHONE" or value == "phone":
            return AssetType.PHONE

        elif value == "MONITOR" or value == "monitor":
            return AssetType.MONITOR

        else:
            print("Invalid type. Please enter Laptop, Monitor, or Phone.")

def get_valid_asset_status(prompt):
    while True:
        value = input(prompt).strip().upper()

        if value.lower() == "c":
            print("Cancelled.")
            return None
        
        elif value == "":
            print("This field cannot be empty. Please try again.")
            continue

        elif value == "AVAILABLE":
            return AssetStatus.AVAILABLE
        
        elif value == "ASSIGNED":
            return AssetStatus.ASSIGNED
        
        elif value == "REPAIR":
            return AssetStatus.REPAIR
        
        elif value == "RETIRED":
            return AssetStatus.RETIRED
        
        else:
            print("Invalid status. Please enter Available, Assigned, Repair, or Retired.")

def get_extra_fields_for_type(asset_type):
    if asset_type == AssetType.LAPTOP:
        ram = get_valid_text("Enter RAM (e.g. 16GB): ")
        storage = get_valid_text("Enter storage (e.g. 512GB): ")
        operating_system = get_valid_text("Enter operating system: ")

        return {"ram": ram, "storage": storage, "operating_system": operating_system}

    elif asset_type == AssetType.MONITOR:
        resolution = get_valid_text("Enter resolution: ")
        screen_size = get_valid_text("Enter screen size: ")
        refresh_rate = get_valid_text("Enter refresh rate: ")

        return {"resolution": resolution, "screen_size": screen_size, "refresh_rate": refresh_rate}

    elif asset_type == AssetType.PHONE:
        ram = get_valid_text("Enter RAM: ")
        storage = get_valid_text("Enter storage: ")
        operating_system = get_valid_text("Enter operating system: ")
        battery = get_valid_text("Enter battery: ")
        processor = get_valid_text("Enter processor: ")
        network = get_valid_text("Enter network: ")

        return {"ram": ram, "storage": storage, "operating_system": operating_system, "battery": battery, "processor": processor, "network": network}

    else:
        return {}

def get_valid_ticket_priority(prompt):
    while True:
        value = input(prompt).upper()

        if value.lower() == "c":
            print("Cancelled.")
            return None
        
        elif value == "":
            print("This field cannot be empty. Please try valuegain.")
            continue

        elif value == "LOW":
            return TicketPriority.LOW

        elif value == "MEDIUM":
            return TicketPriority.MEDIUM

        elif value == "HIGH":
            return TicketPriority.HIGH

        elif value == "CRITICAL":
            return TicketPriority.CRITICAL

        else:
            print("Invalid status. Please enter low, medium, high, or critical")

def get_valid_ticket_status(prompt):
    while True:
        value = input(prompt).upper()

        if value.lower() == "c":
            print("Cancelled.")
            return None
        
        elif value == "":
            print("This field cannot be empty. Please try again.")
            continue

        elif value == "OPEN":
            return TicketStatus.OPEN

        elif value == "IN_PROGRESS":
            return TicketStatus.IN_PROGRESS

        elif value == "RESOLVED":
            return TicketStatus.RESOLVED

        elif value == "CLOSED":
            return TicketStatus.CLOSED

        else:
            print("Invalid status. Please enter open, in progress, resolved, or closed.")