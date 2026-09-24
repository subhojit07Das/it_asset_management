from app.services.employee_service import EmployeeService
from app.services.asset_service import AssetService
from app.utils.enums import AssetType, AssetStatus
from app.services.assignment_service import AssignmentService

service = EmployeeService()

emp1 = service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")
emp2 = service.create_employee(1002, "Gin", "gin@mail.com", "Finance")

new_service = AssetService()

asset1 = new_service.create_asset(1, AssetType.LAPTOP, "DELL", "Dell Latitude 5124", "SN45678", AssetStatus.AVAILABLE)

add_asset = AssignmentService(service, new_service)

print(add_asset.assign_asset(1001, 1))