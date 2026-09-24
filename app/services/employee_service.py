from app.models.employee import Employee

class EmployeeService:
    def __init__(self):
        self.employees = {}

    def create_employee(self, employee_id, name, email, department):
        employee = Employee(employee_id, name, email, department)

        self.employees[employee_id] = employee
        return employee

    def get_employee(self, employee_id):
        return self.employees.get(employee_id)

    def get_all_employees(self):
        return self.employees.values()