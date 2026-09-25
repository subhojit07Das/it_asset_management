from app.models.employee import Employee

class EmployeeRepository:
    def __init__(self):
        self.employees = {}

    def save(self, employee: Employee):
        self.employees[employee.employee_id] = employee
        return employee

    def get_by_id(self, employee_id):
        return self.employees.get(employee_id)

    def get_all(self):
        return self.employees.values()

    def delete(self, employee_id):
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        
        return False

    def exists(self, employee_id):
        return employee_id in self.employees