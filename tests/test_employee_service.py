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

def test_get_all_employees(service):
    employee = service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")

    employee2 = service.create_employee(1002, "Itachi", "itachi@mail.com", "DevOps")

    all_employees = list(service.get_all_employees())

    assert len(all_employees) == 2
    assert employee.name == "Aizen"
    assert employee2.name == "Itachi"
    assert employee in all_employees
    assert employee2 in all_employees