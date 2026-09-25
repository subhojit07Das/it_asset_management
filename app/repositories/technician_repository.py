from app.models.technician import Technician

class TechnicianRepository:
    def __init__(self):
        self.technicians = {}

    def save(self, technician: Technician):
        self.technicians[technician.technician_id] = technician
        return technician

    def get_by_id(self, technician_id):
        return self.technicians.get(technician_id)

    def get_all(self):
        return self.technicians.values()

    def delete(self, technician_id):
        if technician_id in self.technicians:
            del self.technicians[technician_id]
            return True
        
        return False

    def exists(self, technician_id):
        return technician_id in self.technicians