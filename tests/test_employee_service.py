import pytest
from app.services.employee_service import EmployeeService
from app.repositories.employee_repository import EmployeeRepository
from app.exceptions.employee_exceptions import EmployeeNotFoundError, EmployeeAlreadyExistsError

@pytest.fixture
def repo():
    return EmployeeRepository()

@pytest.fixture
def service(repo):
    return EmployeeService(repo)

def test_create_employee(repo, service):
    employee = service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")

    assert employee.employee_id == 1001
    assert employee.name == "Aizen"
    assert repo.exists(1001)

def test_create_employee_duplicate_id_raise(service):
    service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")

    with pytest.raises(EmployeeAlreadyExistsError):
        service.create_employee(1001, "Someone Else", "x@mail.com", "HR")

def test_get_employee_missing_id(service):
    with pytest.raises(EmployeeNotFoundError):
        service.get_employee(9999)