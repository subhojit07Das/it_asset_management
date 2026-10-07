from app.exceptions.employee_exceptions import EmployeeAlreadyExistsError, EmployeeNotFoundError
from cli.helpers.input_helper import get_valid_id, get_valid_text, get_valid_name

def employee_menu(employee_service):
    while True:
        print("\n----- Employee Menu -----")
        print("1) Create Employee \n2) View Employee \n3) View All Employee \n4) Delete Employee \n5) Exit")

        check_choice = input("Choose an option: ")
        if not check_choice.isdigit():
            print("Please the number typed.")
            continue

        choice = int(check_choice)

        if choice == 1:
            create_employee(employee_service)

        elif choice == 2:
            view_employee(employee_service)

        elif choice == 3:
            view_all_employees(employee_service)
        
        elif choice == 4:
            delete_employee(employee_service)

        elif choice == 5:
            break

        else:
            print("Invalid option selected, try again.")

def create_employee(employee_service):
    employee_id = get_valid_id()

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
        employee = employee_service.create_employee(employee_id, name, email, department)
        print(f"Created: {employee}")
    except EmployeeAlreadyExistsError as e:
        print(f"Error: {e}")

def view_employee(employee_service):
    employee_id = get_valid_id()
    
    try:
        save = employee_service.get_employee(employee_id)
        print(f"----- Employee Information {employee_id} -----")
        print(save)
    except EmployeeNotFoundError as e:
        print(f"Error: {e}")

def view_all_employees(employee_service):
    all_employee = employee_service.get_all_employees()
    
    print("\n----- All Employee List -----")
    for item in all_employee:
        print(item)

def delete_employee(employee_service):
    employee_id = get_valid_id()
    
    try:
        employee_service.delete_employee(employee_id)
        print(f"Employee with {employee_id} deleted successfully.")
    except EmployeeNotFoundError as e:
        print(f"Error: {e}")

