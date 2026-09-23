from app.models.asset import Asset
from app.utils.enums import AssetType

class Monitor(Asset):
    def __init__(self, asset_id, brand, model, serial_number, status, resolution, screen_size, refresh_rate):

        super().__init__(asset_id, AssetType.MONITOR, brand, model, serial_number, status)

        self.resolution = resolution
        self.screen_size = screen_size
        self.refresh_rate = refresh_rate

    def __str__(self):
        return f"{super().__str__()} \nResolution: {self.resolution} \nScreen Size: {self.screen_size} \nRefresh Rate: {self.refresh_rate}"