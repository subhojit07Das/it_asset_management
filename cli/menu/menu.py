from cli.menu.employee_menu import employee_menu
from cli.menu.asset_menu import asset_menu
from cli.menu.technician_menu import technician_menu
from cli.menu.ticket_menu import ticket_menu
from cli.menu.assignment_menu import assignment_menu

def main_menu(employee_service, asset_service, technician_service, ticket_service, assignment_service):
    while True:
        print("\n=== IT Asset Management System ===")
        print("1. Employee Menu")
        print("2. Asset Menu")
        print("3. Technician Menu")
        print("4. Ticket Menu")
        print("5. Assignment Menu")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            employee_menu(employee_service)
        elif choice == "2":
            asset_menu(asset_service)
        elif choice == "3":
            technician_menu(technician_service)
        elif choice == "4":
            ticket_menu(ticket_service, employee_service, asset_service, technician_service)
        elif choice == "5":
            assignment_menu(assignment_service)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")
