from app.models.asset import Asset
from app.models.laptop import Laptop
from app.models.monitor import Monitor
from app.models.phone import Phone
from app.utils.enums import AssetType
from app.repositories.asset_repository import AssetRepository

class AssetService:
    def __init__(self, assets: AssetRepository):
        self.assets = assets

    def create_asset(self, asset_id, asset_type, brand, model, serial_number, status, **extra_fields):
        if asset_type == AssetType.LAPTOP:
            asset = Laptop(asset_id, brand, model, serial_number, status, **extra_fields)
        elif asset_type == AssetType.MONITOR:
            asset = Monitor(asset_id, brand, model, serial_number, status, **extra_fields)
        elif asset_type == AssetType.PHONE:
            asset = Phone(asset_id, brand, model, serial_number, status, **extra_fields)
        else:
            asset = Asset(asset_id, asset_type, brand, model, serial_number, status)

        self.assets.save(asset)
        return asset

    def get_asset(self, asset_id):
        return self.assets.get_by_id(asset_id)

    def get_all_assets(self):
        return self.assets.get_all()

    def delete_asset(self, asset_id):
        return self.assets.delete(asset_id)

    def check_asset(self, asset_id):
        return self.assets.exists(asset_id)