from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository

class EmployeeService:
    def __init__(self, employees: EmployeeRepository):
        self.employees = employees

    def create_employee(self, employee_id, name, email, department):
        employee = Employee(employee_id, name, email, department)

        self.employees.save(employee)
        return employee

    def get_employee(self, employee_id):
        return self.employees.get_by_id(employee_id)

    def get_all_employees(self):
        return self.employees.get_all()

    def delete_employee(self, employee_id):
        return self.employees.delete(employee_id)

    def check_employee(self, employee_id):
        return self.employees.exists(employee_id)

    