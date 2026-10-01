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