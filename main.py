from app.services.employee_service import EmployeeService
from app.services.asset_service import AssetService
from app.services.technician_service import TechnicianService
from app.services.ticket_service import TicketService
from app.utils.enums import AssetType, AssetStatus, TicketStatus, TicketPriority

employee_service = EmployeeService()
asset_service = AssetService()
technician_service = TechnicianService()
ticket_service = TicketService(technician_service) 

emp1 = employee_service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")

asset1 = asset_service.create_asset(
    1, AssetType.LAPTOP, "DELL", "Dell Latitude 5124", "SN45678", AssetStatus.AVAILABLE,
    ram="16GB", storage="512GB SSD", operating_system="Windows 11"
)

tech1 = technician_service.create_technician(1, "Uchiha", "uchiha@tech1.com", "IT Support")

ticket1 = ticket_service.create_ticket(
    1, emp1, asset1, "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN
)

print(ticket1)
print()

result = ticket_service.assign_technician(1, 1)
print("After assigning technician:")
print(result)
print()

bad_result = ticket_service.assign_technician(999, 1)
print(f"Assigning to a ticket that doesn't exist: {bad_result}")

second_attempt = ticket_service.assign_technician(1, 1)
print(f"Second assign attempt (ticket still OPEN): {second_attempt}")