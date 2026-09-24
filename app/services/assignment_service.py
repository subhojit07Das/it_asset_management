from app.services.employee_service import EmployeeService
from app.services.asset_service import AssetService
from app.utils.enums import AssetStatus

class AssignmentService:
    def __init__(self, employee_service, asset_service):
        self.employee_service = employee_service
        self.asset_service = asset_service

    def assign_asset(self, employee_id, asset_id):
        employee = self.employee_service.get_employee(employee_id)
        asset = self.asset_service.get_asset(asset_id)

        if asset is None or employee is None:
            return None

        if asset.status != AssetStatus.AVAILABLE:
            return None

        employee.add_asset(asset)
        asset.status = AssetStatus.ASSIGNED

        return asset

    def unassign_asset(self, employee_id, asset_id):
        employee = self.employee_service.get_employee(employee_id)
        asset = self.asset_service.get_asset(asset_id)

        if asset is None or employee is None:
            return None

        if asset.status != AssetStatus.ASSIGNED:
            return None

        employee.remove_asset(asset)
        asset.status = AssetStatus.AVAILABLE

        return asset