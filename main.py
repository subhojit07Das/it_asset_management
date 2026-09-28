from app.services.employee_service import EmployeeService
from app.repositories.employee_repository import EmployeeRepository
from app.utils.enums import AssetType, AssetStatus
from app.services.asset_service import AssetService
from app.repositories.asset_repository import AssetRepository
from app.services.technician_service import TechnicianService
from app.repositories.technician_repository import TechnicianRepository
from app.services.ticket_service import TicketService
from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository
from app.utils.enums import TicketPriority, TicketStatus   
from app.exceptions.employee_exceptions import EmployeeNotFoundError, EmployeeAlreadyExistsError
from app.exceptions.asset_exceptions import AssetAlreadyExistsError, AssetNotFoundError
from app.exceptions.technician_exceptions import TechnicianNotFoundError, TechnicianAlreadyExistsError
from app.services.assignment_service import AssignmentService
from app.exceptions.assignment_exceptions import AssetNotAvailableError, AssetNotAssignedError, AssetNotAssignedToEmployeeError
from app.exceptions.ticket_exceptions import TicketNotFoundError, TicketNotOpenError, TicketAlreadyExistsError

employee = EmployeeRepository()
service = EmployeeService(employee)
ser1 = AssetRepository()
asset = AssetService(ser1)
tech_serv = TechnicianRepository()
technician = TechnicianService(tech_serv)   
ticket_repo = TicketRepository()             
tick = TicketService(technician, ticket_repo)  

emp1 = service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")

new_asset1 = asset.create_asset(1, AssetType.LAPTOP, "Dell", "Latitude 512", "SN567534", AssetStatus.ASSIGNED, ram="16GB", storage="512GB", operating_system="Windows 11")

tech1 = technician.create_technician(1, "Uchiha", "uchiha@tech1@gmail.com", "IT Support")

ticket1 = tick.create_ticket(
    1,
    emp1,
    new_asset1,
    "Laptop won't boot",
    TicketPriority.HIGH,
    TicketStatus.OPEN
)

print(ticket1)

print(ticket1)
print()

assigned = tick.assign_technician(1, 1)
print(f"Status after assignment: {assigned.status}")

print()

# Ticket 1 is now IN_PROGRESS, so assigning again should fail
try:
    tick.assign_technician(1, 1)
except TicketNotOpenError as e:
    print(f"Caught an error: {e}")

print()

# Ticket 999 doesn't exist
try:
    tick.assign_technician(999, 1)
except TicketNotFoundError as e:
    print(f"Caught an error: {e}")

print()

# Ticket exists, technician 999 doesn't
try:
    tick.assign_technician(1, 999)
except TechnicianNotFoundError as e:
    print(f"Caught an error: {e}")

print()

# Ticket ID 1 already exists, so creating it again should fail
try:
    tick.create_ticket(
        1, emp1, new_asset1, "Duplicate ticket", TicketPriority.LOW, TicketStatus.OPEN
    )
except TicketAlreadyExistsError as e:
    print(f"Caught an error: {e}")

print()

try:
    ghost = service.get_employee(9999)
    print(ghost)
except EmployeeNotFoundError as e:
    print(f"Caught an error: {e}")

print()
# broken = service.get_employee(9999)
# print(broken)

try:
    duplicate = service.create_employee(1001, "Someone Else", "x@mail.com", "HR")
except EmployeeAlreadyExistsError as e:
    print(f"Caught an error: {e}")

# Test AssetNotFoundError — asset_id 999 shouldn't exist
try:
    ghost_asset = asset.get_asset(999)
    print(ghost_asset)
except AssetNotFoundError as e:
    print(f"Caught an error: {e}")

print()

# Test AssetAlreadyExistsError — asset_id 1 already exists
try:
    duplicate_asset = asset.create_asset(
        1, AssetType.LAPTOP, "HP", "EliteBook", "SN000000", AssetStatus.AVAILABLE,
        ram="8GB", storage="256GB", operating_system="Windows 10"
    )
except AssetAlreadyExistsError as e:
    print(f"Caught an error: {e}")


    # Test TechnicianNotFoundError — technician_id 999 shouldn't exist
try:
    ghost_technician = technician.get_technician(999)
    print(ghost_technician)
except TechnicianNotFoundError as e:
    print(f"Caught an error: {e}")

print()

# Test TechnicianAlreadyExistsError — technician_id 1 already exists
try:
    duplicate_technician = technician.create_technician(1, "Someone Else", "y@mail.com", "IT Support")
except TechnicianAlreadyExistsError as e:
    print(f"Caught an error: {e}")

assignment = AssignmentService(service, asset)

# Case A: asset 1 has status ASSIGNED but was never added to Aizen's list
try:
    assignment.unassign_asset(1001, 1)
except AssetNotAssignedToEmployeeError as e:
    print(f"Caught an error: {e}")

print()

# Case B setup: a fresh AVAILABLE asset and a second employee
spare = asset.create_asset(
    2, AssetType.LAPTOP, "HP", "EliteBook", "SN000002", AssetStatus.AVAILABLE,
    ram="8GB", storage="256GB", operating_system="Windows 10"
)
other = service.create_employee(1002, "Kurosaki", "kurosaki@mail.com", "HR")
assignment.assign_asset(1001, 2)

# Case B: a different employee tries to unassign Aizen's asset
try:
    assignment.unassign_asset(1002, 2)
except AssetNotAssignedToEmployeeError as e:
    print(f"Caught an error: {e}")

print()

# Case C: the rightful owner unassigns it, which should succeed
result = assignment.unassign_asset(1001, 2)
print(f"Unassigned: {result.status}")