from app.models.employee import Employee
from app.utils.enums import AssetStatus
from app.models.laptop import Laptop
from app.models.monitor import Monitor
from app.models.phone import Phone

emp1 = Employee(1001, "Aizen", "aizen@mail.com", "IT")
emp2 = Employee(1002, "Itachi", "itachi@mail.com", "SALES")

laptop = Laptop(
    asset_id=1,
    brand="Dell",
    model="Latitude 5420",
    serial_number="SN12345",
    status=AssetStatus.AVAILABLE,
    ram="16GB",
    storage="512GB SSD",
    operating_system="Windows 11"
)

monitor = Monitor(
    asset_id=2,
    brand="HP",
    model="HP Series 5 27 FHD",
    serial_number="SRN4567",
    status=AssetStatus.AVAILABLE,
    resolution="1920x1080p",
    screen_size="24 inches",
    refresh_rate="60 hz"
)

phone = Phone(
    asset_id=3,
    brand="Apple",
    model="Iphone 17",
    serial_number="SRN7890",
    status=AssetStatus.AVAILABLE,
    ram="8GB",
    storage="256GB",
    operating_system="IOS 26.6",
    battery="3900mAh",
    processor="A19 Chip",
    network="5G"
)

emp1.add_asset(laptop)
for asset1 in emp1.assigned_assets:
    print(asset1)

print()

emp1.add_asset(monitor)
for asset2 in emp1.assigned_assets:
    print(asset2)

print()

emp1.add_asset(phone)
for asset3 in emp1.assigned_assets:
    print(asset3)

print()

emp2.add_asset(monitor)
for asset in emp2.assigned_assets:
    print(asset)
