from app.utils.enums import AssetStatus, AssetType

class Asset:
    def __init__(self, asset_id, asset_type: "AssetType", brand, model, serial_number, status: "AssetStatus"):
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.brand = brand
        self.model = model
        self.serial_number = serial_number
        self.status = status

    def __str__(self):
        return f"Asset({self.asset_id}): {self.asset_type} - {self.brand} - {self.model} - {self.serial_number} - {self.status}"