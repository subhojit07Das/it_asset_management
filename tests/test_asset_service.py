import pytest
from app.exceptions.asset_exceptions import AssetAlreadyExistsError, AssetNotFoundError
from app.services.asset_service import AssetService
from app.repositories.asset_repository import AssetRepository
from app.utils.enums import AssetStatus, AssetType

@pytest.fixture
def repo():
    return AssetRepository()

@pytest.fixture
def service(repo):
    return AssetService(repo)

def test_create_asset(repo, service):
    asset = service.create_asset(1, AssetType.MONITOR, "HP", "HP Omen HyperX", "SN789543", AssetStatus.REPAIR, resolution="1920x1080px", screen_size="32 Inches", refresh_rate="60 hz")

    assert asset.asset_id == 1
    assert asset.status == AssetStatus.REPAIR
    assert asset.refresh_rate == "60 hz"
    assert repo.exists(1)

def test_create_asset_duplicate_id_raise(service):
    service.create_asset(1, AssetType.MONITOR, "HP", "HP Omen HyperX", "SN789543", AssetStatus.REPAIR, resolution="1920x1080px", screen_size="32 Inches", refresh_rate="60 hz")

    with pytest.raises(AssetAlreadyExistsError):
        service.create_asset(1, AssetType.MONITOR, "HP", "Something else", "SN789543", AssetStatus.AVAILABLE, resolution="1920x1080px", screen_size="32 Inches", refresh_rate="60 hz")

def test_get_asset_missing_id(service):
    with pytest.raises(AssetNotFoundError):
        service.get_asset(0)

def test_delete_asset_missing_id(service):
    with pytest.raises(AssetNotFoundError):
        service.delete_asset(1)

def test_check_asset(service):
    service.create_asset(1, AssetType.MONITOR, "HP", "HP Omen HyperX", "SN789543", AssetStatus.REPAIR, resolution="1920x1080px", screen_size="32 Inches", refresh_rate="60 hz")

    assert service.check_asset(1) is True
    assert service.check_asset(999) is False

def test_create_asset_phone(repo, service):
    phone = service.create_asset(1, AssetType.PHONE, "Apple", "Iphone 17", "SN98646423", AssetStatus.AVAILABLE, ram="8GB", storage="256GB", operating_system="IOS 27", battery="3924 MAH", processor="A19", network="5G")

    assert phone.asset_id == 1
    assert phone.status == AssetStatus.AVAILABLE
    assert repo.exists(1)

def test_get_all_assets(repo, service):
    phone = service.create_asset(1, AssetType.PHONE, "Apple", "Iphone 17", "SN98646423", AssetStatus.AVAILABLE, ram="8GB", storage="256GB", operating_system="IOS 27", battery="3924 MAH", processor="A19", network="5G")

    monitor = service.create_asset(2, AssetType.MONITOR, "HP", "HP Omen HyperX", "SN789543", AssetStatus.REPAIR, resolution="1920x1080px", screen_size="32 Inches", refresh_rate="60 hz")

    laptop = service.create_asset(3, AssetType.LAPTOP, "Dell", "Dell Vostro 5625U", "SN98646423", AssetStatus.AVAILABLE, ram="16GB", storage="1TB", operating_system="Window 11 Pro")

    all_assets = list(service.get_all_assets())

    assert len(all_assets) == 3
    assert phone.battery == "3924 MAH"
    assert phone in all_assets
    assert monitor in all_assets
    assert laptop in all_assets