from app.services.employee_service import EmployeeService

service = EmployeeService()

emp1 = service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")
emp2 = service.create_employee(1002, "Gin", "gin@mail.com", "Finance")

for emp_id in service.employees.items():
    print(emp_id)

get_all = service.get_all_employees()
for employee in get_all:
    print(employee)