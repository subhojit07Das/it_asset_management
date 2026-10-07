from app.exceptions.technician_exceptions import TechnicianAlreadyExistsError, TechnicianNotFoundError
from cli.helpers.input_helper import get_valid_id, get_valid_name, get_valid_text

def technician_menu(technician_service):
    while True:
        print("\n----- Technician Menu -----")
        print("1) Create Technician \n2) View Technician \n3) View All Technician \n4) Delete Technician \n5) Exit")

        check_choice = input("Choose an option: ")
        if not check_choice.isdigit():
            print("Please the number typed.")
            continue

        choice = int(check_choice)

        if choice == 1:
            create_technician(technician_service)

        elif choice == 2:
            view_technician(technician_service)

        elif choice == 3:
            view_all_technician(technician_service)
        
        elif choice == 4:
            delete_technician(technician_service)

        elif choice == 5:
            break

        else:
            print("Invalid option selected, try again.")

def create_technician(technician_service):
    technician_id = get_valid_id()

    name = get_valid_name("Please enter your name (or 'c' to cancel): ")
    if name is None:
        return

    email = get_valid_text("Please enter your email id (or 'c' to cancel): ")
    if email is None:
        return

    department = get_valid_text("Please enter your department (or 'c' to cancel): ")
    if department is None:
        return

    try:
        technician = technician_service.create_technician(technician_id, name, email, department)
        print(f"Created: {technician}")
    except TechnicianAlreadyExistsError as e:
        print(f"Error: {e}")

def view_technician(technician_service):
    technician_id = get_valid_id()
    
    try:
        save = technician_service.get_technician(technician_id)
        print(f"----- Technician Information {technician_id} -----")
        print(save)
    except TechnicianNotFoundError as e:
        print(f"Error: {e}")

def view_all_technician(technician_service):
    all_technician = technician_service.get_all_technicians()
    
    print("\n----- All Technician List -----")
    for item in all_technician:
        print(item)

def delete_technician(technician_service):
    technician_id = get_valid_id()
    
    try:
        technician_service.delete_technician(technician_id)
        print(f"Technician with {technician_id} deleted successfully.")
    except TechnicianNotFoundError as e:
        print(f"Error: {e}")