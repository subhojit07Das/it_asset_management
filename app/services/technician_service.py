from app.repositories.technician_repository import TechnicianRepository
from app.models.technician import Technician

class TechnicianService:
    def __init__(self, technicians: TechnicianRepository):
        self.technicians = technicians

    def create_technician(self, technician_id, name, email, department):
        technician = Technician(technician_id, name, email, department)

        self.technicians.save(technician)
        return technician

    def get_technician(self, technician_id):
        return self.technicians.get_by_id(technician_id)

    def get_all_technicians(self):
        return self.technicians.get_all()

    def delete_technician(self, technician_id):
        return self.technicians.delete(technician_id)

    def check_technician(self, technician_id):
        return self.technicians.exists(technician_id)