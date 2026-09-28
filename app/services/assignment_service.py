from app.services.employee_service import EmployeeService
from app.services.asset_service import AssetService
from app.utils.enums import AssetStatus
from app.exceptions.assignment_exceptions import AssetNotAssignedError, AssetNotAvailableError, AssetNotAssignedToEmployeeError

class AssignmentService:
    def __init__(self, employee_service, asset_service):
        self.employee_service = employee_service
        self.asset_service = asset_service

    def assign_asset(self, employee_id, asset_id):
        employee = self.employee_service.get_employee(employee_id)
        asset = self.asset_service.get_asset(asset_id)

        if asset.status != AssetStatus.AVAILABLE:
            raise AssetNotAvailableError(f"Asset ID: {asset_id} not available. Current status is {asset.status}")
       
        employee.add_asset(asset)
        asset.status = AssetStatus.ASSIGNED

        return asset

    def unassign_asset(self, employee_id, asset_id):
        employee = self.employee_service.get_employee(employee_id)
        asset = self.asset_service.get_asset(asset_id)

        if asset.status != AssetStatus.ASSIGNED:
            raise AssetNotAssignedError(f"Asset ID: {asset_id} not assigned yet. Current status is {asset.status}")

        if asset not in employee.assigned_assets:
            raise AssetNotAssignedToEmployeeError(f"Asset ID: {asset_id} is not assigned to employee ID: {employee_id}")

        employee.remove_asset(asset)
        asset.status = AssetStatus.AVAILABLE

        return asset