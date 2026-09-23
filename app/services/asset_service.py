from app.models.asset import Asset

class AssetService:
    def __init__(self):
        self.assets = {}

    def create_asset(self, asset_id, asset_type, brand, model, serial_number, status):
        asset = Asset(asset_id, asset_type, brand, model, serial_number, status)

        self.assets[asset_id] = asset
        return asset

    def get_asset(self, asset_id):
        asset = self.assets[asset_id]

        return asset

    def get_all_assets(self):
        return self.assets.values()