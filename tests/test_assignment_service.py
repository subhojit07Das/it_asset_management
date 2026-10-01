import pytest
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.repositories.asset_repository import AssetRepository
from app.services.asset_service import AssetService
from app.services.assignment_service import AssignmentService
from app.utils.enums import AssetStatus, AssetType
from app.exceptions.assignment_exceptions import AssetNotAssignedError, AssetNotAssignedToEmployeeError, AssetNotAvailableError

@pytest.fixture
def employee_repo():
    return EmployeeRepository()

@pytest.fixture
def employee_service(employee_repo):
    return EmployeeService(employee_repo)

@pytest.fixture
def asset_repo():
    return AssetRepository()

@pytest.fixture
def asset_service(asset_repo):
    return AssetService(asset_repo)

@pytest.fixture
def assignment_service(employee_service, asset_service):
    return AssignmentService(employee_service, asset_service)

def test_assign_asset_success(assignment_service, employee_service, asset_service):
    employee = employee_service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")
    
    asset = asset_service.create_asset(1, AssetType.MONITOR, "HP", "HP Omen HyperX", "SN789543", AssetStatus.AVAILABLE, resolution="1920x1080px", screen_size="32 Inches", refresh_rate="60 hz")

    store = assignment_service.assign_asset(employee.employee_id, asset.asset_id)

    assert store.status == AssetStatus.ASSIGNED
    assert asset in employee.assigned_assets

def test_assign_asset_not_available_raises(assignment_service, employee_service, asset_service):
    employee = employee_service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")
        
    asset = asset_service.create_asset(1, AssetType.MONITOR, "HP", "HP Omen HyperX", "SN789543", AssetStatus.ASSIGNED, resolution="1920x1080px", screen_size="32 Inches", refresh_rate="60 hz")

    with pytest.raises(AssetNotAvailableError):
        assignment_service.assign_asset(employee.employee_id, asset.asset_id)

def test_unassign_asset_not_assigned_raises(assignment_service, employee_service, asset_service):
    employee = employee_service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")
    
    asset = asset_service.create_asset(1, AssetType.MONITOR, "HP", "HP Omen HyperX", "SN789543", AssetStatus.AVAILABLE, resolution="1920x1080px", screen_size="32 Inches", refresh_rate="60 hz")

    with pytest.raises(AssetNotAssignedError):
        assignment_service.unassign_asset(employee.employee_id, asset.asset_id)

def test_unassign_asset_wrong_employee_raises(assignment_service, employee_service, asset_service):
    employee = employee_service.create_employee(1001, "Aizen", "aizen@mail.com", "IT")
    employee2 = employee_service.create_employee(1002, "Itachi", "itachi@mail.com", "IT Support")
        
    asset = asset_service.create_asset(1, AssetType.MONITOR, "HP", "HP Omen HyperX", "SN789543", AssetStatus.AVAILABLE, resolution="1920x1080px", screen_size="32 Inches", refresh_rate="60 hz")

    store = assignment_service.assign_asset(employee.employee_id, asset.asset_id)

    assert store.status == AssetStatus.ASSIGNED
    assert asset in employee.assigned_assets

    with pytest.raises(AssetNotAssignedToEmployeeError):
        assignment_service.unassign_asset(employee2.employee_id, asset.asset_id)