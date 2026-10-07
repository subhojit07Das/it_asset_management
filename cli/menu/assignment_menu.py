from app.exceptions.assignment_exceptions import (
    AssetNotAssignedError, AssetNotAssignedToEmployeeError, AssetNotAvailableError
)
from app.exceptions.employee_exceptions import EmployeeNotFoundError
from app.exceptions.asset_exceptions import AssetNotFoundError
from cli.helpers.input_helper import get_valid_id

def assignment_menu(assignment_service):
    while True:
        print("\n----- Assignment Menu -----")
        print("1) Assign Asset to Employee \n2) Unassign Asset from Employee \n3) Exit")

        check_choice = input("Choose an option: ")
        if not check_choice.isdigit():
            print("Please enter a valid number.")
            continue

        choice = int(check_choice)

        if choice == 1:
            assign_asset(assignment_service)
        elif choice == 2:
            unassign_asset(assignment_service)
        elif choice == 3:
            break
        else:
            print("Invalid option selected, try again.")

def assign_asset(assignment_service):
    employee_id = get_valid_id("Please enter employee ID: ")
    asset_id = get_valid_id("Please enter asset ID: ")

    try:
        asset = assignment_service.assign_asset(employee_id, asset_id)
        print(f"Asset {asset_id} assigned to employee {employee_id}. Status: {asset.status}")
    except (EmployeeNotFoundError, AssetNotFoundError, AssetNotAvailableError) as e:
        print(f"Error: {e}")

def unassign_asset(assignment_service):
    employee_id = get_valid_id("Please enter employee ID: ")
    asset_id = get_valid_id("Please enter asset ID: ")

    try:
        asset = assignment_service.unassign_asset(employee_id, asset_id)
        print(f"Asset {asset_id} unassigned from employee {employee_id}. Status: {asset.status}")
    except (EmployeeNotFoundError, AssetNotFoundError,
            AssetNotAssignedError, AssetNotAssignedToEmployeeError) as e:
        print(f"Error: {e}")