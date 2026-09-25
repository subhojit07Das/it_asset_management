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

employee = EmployeeRepository()
service = EmployeeService(employee)
ser1 = AssetRepository()
asset = AssetService(ser1)
tech_serv = TechnicianRepository()
technician = TechnicianService(tech_serv)   # the actual service
ticket_repo = TicketRepository()             # the actual repository
tick = TicketService(technician, ticket_repo)  # service gets: (technician_service, ticket_repository)


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

assigned = tick.assign_technician(1, 1)
print(assigned)
print()

already_assigned = tick.assign_technician(1, 1)
print(already_assigned)
print()

# Try assigning to a ticket that doesn't exist — should return None
missing_ticket = tick.assign_technician(999, 1)
print(missing_ticket)