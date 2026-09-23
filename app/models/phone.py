from app.models.asset import Asset
from app.utils.enums import AssetType

class Phone(Asset):
    def __init__(self, asset_id, brand, model, serial_number, status, ram, storage, operating_system, battery, processor, network):

        super().__init__(asset_id, AssetType.PHONE, brand, model, serial_number, status)

        self.ram = ram
        self.storage = storage
        self.operating_system = operating_system
        self.battery = battery
        self.processor = processor
        self.network = network

    def __str__(self):
        return f"{super().__str__()} \nRam: {self.ram} \nStorage: {self.storage} \nOperating System: {self.operating_system} \nBattery: {self.battery} \nProcessor: {self.processor} \nNetwork: {self.network}"