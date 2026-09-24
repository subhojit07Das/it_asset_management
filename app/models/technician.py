class Technician:
    def __init__(self, technician_id, name, email, department):
        self.technician_id = technician_id
        self.name = name
        self.email = email
        self.department = department

    def __str__(self):
        return f"Technician ID: {self.technician_id} \nName: {self.name} \nEmail: {self.email} \nDepartment: {self.department}"