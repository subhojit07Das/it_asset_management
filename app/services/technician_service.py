from app.repositories.technician_repository import TechnicianRepository
from app.models.technician import Technician
from app.exceptions.technician_exceptions import TechnicianAlreadyExistsError, TechnicianNotFoundError

class TechnicianService:
    def __init__(self, technicians: TechnicianRepository):
        self.technicians = technicians

    def create_technician(self, technician_id, name, email, department):
        if self.technicians.exists(technician_id):
            raise TechnicianAlreadyExistsError(f"Technician with {technician_id} already exists.")

        technician = Technician(technician_id, name, email, department)

        self.technicians.save(technician)
        return technician

    def get_technician(self, technician_id):
        techinician = self.technicians.get_by_id(technician_id)
        if techinician is None:
            raise TechnicianNotFoundError(f"Technician with {technician_id} not found.")

        return techinician

    def get_all_technicians(self):
        return self.technicians.get_all()

    def delete_technician(self, technician_id):
        technician = self.technicians.get_by_id(technician_id)
        if technician is None:
            raise TechnicianNotFoundError(f"Technician with {technician_id} not found.")

        return self.technicians.delete(technician_id)

    def check_technician(self, technician_id):
        return self.technicians.exists(technician_id)