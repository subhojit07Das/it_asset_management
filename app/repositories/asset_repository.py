from app.models.asset import Asset

class AssetRepository:
    def __init__(self):
        self.assets = {}

    def save(self, asset: Asset):
        self.assets[asset.asset_id] = asset
        return asset

    def get_by_id(self, asset_id):
        return self.assets.get(asset_id)

    def get_all(self):
        return self.assets.values()

    def delete(self, asset_id):
        if asset_id in self.assets:
            del self.assets[asset_id]
            return True
        
        return False

    def exists(self, asset_id):
        return asset_id in self.assets