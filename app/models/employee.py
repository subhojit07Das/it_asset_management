from app.models.asset import Asset

class Employee:
    def __init__(self, employee_id, name, email, department):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.department = department
        self.assigned_assets = []

    def __str__(self):
        return f"Employee({self.employee_id}): {self.name} - {self.email} - {self.department}"

    def add_asset(self, asset: Asset):
        self.assigned_assets.append(asset)