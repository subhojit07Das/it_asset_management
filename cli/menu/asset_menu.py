from app.exceptions.asset_exceptions import AssetAlreadyExistsError, AssetNotFoundError
from cli.helpers.input_helper import get_valid_id, get_valid_text, get_valid_asset_type, get_valid_asset_status, get_extra_fields_for_type

def asset_menu(asset_service):
    while True:
        print("\n----- Asset Menu -----")
        print("1) Create Asset \n2) View Asset \n3) View All Assets \n4) Delete Asset \n5) Exit")

        check_choice = input("Choose an option: ")
        if not check_choice.isdigit():
            print("Please the number typed.")
            continue

        choice = int(check_choice)

        if choice == 1:
            create_asset(asset_service)

        elif choice == 2:
            view_asset(asset_service)

        elif choice == 3:
            view_all_assets(asset_service)
        
        elif choice == 4:
            delete_asset(asset_service)

        elif choice == 5:
            break

        else:
            print("Invalid option selected, try again.")

def create_asset(asset_service):
    asset_id = get_valid_id()

    asset_type = get_valid_asset_type("Please enter asset type as 'Laptop', 'Monitor' or 'Phone' (or 'c' to cancel): ")
    if asset_type is None:
        return
        
    brand = get_valid_text("Please enter brand (or 'c' to cancel): ")
    if brand is None:
        return
        
    model  = get_valid_text("Please enter model (or 'c' to cancel): ")
    if model is None:
        return
        
    serial_number = get_valid_text("Please enter serial number (or 'c' to cancel): ")
    if serial_number is None:
        return
    
    status = get_valid_asset_status("Please enter status (or 'c' to cancel): ")
    if status is None:
        return

    extra_fields = get_extra_fields_for_type(asset_type)

    try:
        asset = asset_service.create_asset(asset_id, asset_type, brand, model, serial_number, status, **extra_fields)
        print(f"Created: {asset}")
    except AssetAlreadyExistsError as e:
        print(f"Error: {e}")

def view_asset(asset_service):
    asset_id = get_valid_id()

    try:
        save = asset_service.get_asset(asset_id)
        print(f"----- Asset Information {asset_id} -----")
        print(save)
    except AssetNotFoundError as e:
        print(f"Error: {e}")

def view_all_assets(asset_service):
    all_asset = asset_service.get_all_assets()

    print("\n----- All Asset List -----")
    for item in all_asset:
        print(item)

def delete_asset(asset_service):
    asset_id = get_valid_id()

    try:
        asset_service.delete_asset(asset_id)
        print(f"Asset with {asset_id} deleted successfully.")
    except AssetNotFoundError as e:
        print(f"Error: {e}")