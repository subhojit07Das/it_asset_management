from app.models.technician import Technician

class TechnicianService:
    def __init__(self):
        self.technicians = {}

    def create_technician(self, technician_id, name, email, department):
        technician = Technician(technician_id, name, email, department)

        self.technicians[technician_id] = technician
        return technician

    def get_technician(self, technician_id):
        return self.technicians.get(technician_id)

    def get_all_technicians(self):
        return self.technicians.values()