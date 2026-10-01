import pytest
from app.services.technician_service import TechnicianService 
from app.repositories.technician_repository import TechnicianRepository
from app.exceptions.technician_exceptions import TechnicianAlreadyExistsError, TechnicianNotFoundError

@pytest.fixture
def repo():
    return TechnicianRepository()

@pytest.fixture
def service(repo):
    return TechnicianService(repo)

def test_create_technician(service, repo):
    technician = service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    assert technician.technician_id == 100
    assert technician.department == "IT Support"
    assert repo.exists(100)

def test_create_technician_duplicate_id_raise(service):
    service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    with pytest.raises(TechnicianAlreadyExistsError):
        service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

def test_get_technician_missing_id(service):
    with pytest.raises(TechnicianNotFoundError):
        service.get_technician(200)

def test_delete_technician_missing_id(service):
    with pytest.raises(TechnicianNotFoundError):
        service.delete_technician(200)

def test_check_technician(service):
    service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    assert service.check_technician(100) is True
    assert service.check_technician(2000) is False

def test_get_all_technicians(service):
    technician = service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    technician1 = service.create_technician(101, "Techy2", "techy2@mail.com", "IT Support")

    all_technicians = list(service.get_all_technicians())

    assert len(all_technicians) == 2
    assert technician in all_technicians
    assert technician1 in all_technicians