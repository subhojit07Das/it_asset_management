from app.services.employee_service import EmployeeService
from app.services.asset_service import AssetService
from app.utils.enums import AssetType, AssetStatus

service = EmployeeService()

emp1 = service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")
emp2 = service.create_employee(1002, "Gin", "gin@mail.com", "Finance")

for emp_id in service.employees.items():
    print(emp_id)

get_all = service.get_all_employees()
for employee in get_all:
    print(employee)

new_service = AssetService()

asset1 = new_service.create_asset(1, AssetType.LAPTOP, "DELL", "Dell Latitude 5124", "SN45678", AssetStatus.ASSIGNED)

print(asset1)

print(new_service.get_assets(1))

assets = new_service.get_all_assets()
for asset in assets:
    print(asset)
