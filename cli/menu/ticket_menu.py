from app.exceptions.ticket_exceptions import (
    TicketAlreadyExistsError, TicketNotFoundError, TicketNotOpenError,
    CommentEmptyError, TicketClosedError,
    TechnicianNotAssignedError, TicketNotInProgressError,
    TicketNotConfirmedError, TicketNotResolvedError, EmployeeNotTicketOwnerError, 
    TicketAlreadyConfirmedError
)
from app.exceptions.technician_exceptions import TechnicianNotFoundError
from app.exceptions.employee_exceptions import EmployeeNotFoundError
from app.exceptions.asset_exceptions import AssetNotFoundError
from app.utils.enums import TicketStatus
from cli.helpers.input_helper import (
    get_valid_id, get_valid_name, get_valid_text, get_valid_ticket_priority, get_valid_yes_no
)

def ticket_menu(ticket_service, employee_service, asset_service, technician_service):
    while True:
        print("\n----- Ticket Menu -----")
        print("1) Create Ticket \n2) View Ticket \n3) View All Tickets \n4) Assign Tickets \n5) Add Comment \n6) Resolve Ticket \n7) Confirm Resolution \n8) Close Ticket \n0) Exit")

        check_choice = input("Choose an option: ")
        if not check_choice.isdigit():
            print("Please enter a valid number.")
            continue

        choice = int(check_choice)

        if choice == 1:
            create_ticket(ticket_service, employee_service, asset_service)

        elif choice == 2:
            view_ticket(ticket_service)

        elif choice == 3:
            view_all_tickets(ticket_service)

        elif choice == 4:
            assign_ticket(ticket_service)

        elif choice == 5:
            add_comment(ticket_service)

        elif choice == 6:
            resolve_ticket(ticket_service)

        elif choice == 7:
            confirm_resolution(ticket_service)

        elif choice == 8:
            close_ticket(ticket_service)

        elif choice == 0:
            break

        else:
            print("Invalid option selected, try again.")

def create_ticket(ticket_service, employee_service, asset_service):
    ticket_id = get_valid_id("Enter ticket ID: ")

    employee_id = get_valid_id("Enter employee ID: ")
    try:
        employee = employee_service.get_employee(employee_id)
    except EmployeeNotFoundError as e:
        print(f"Error: {e}")
        return

    asset_id = get_valid_id("Enter asset ID: ")
    try:
        asset = asset_service.get_asset(asset_id)
    except AssetNotFoundError as e:
        print(f"Error: {e}")
        return

    problem = get_valid_text("Describe the problem (or 'c' to cancel): ")
    if problem is None:
        return

    priority = get_valid_ticket_priority("Enter priority (Low, Medium, High, Critical) (or 'c' to cancel): ")
    if priority is None:
        return

    try:
        ticket = ticket_service.create_ticket(ticket_id, employee, asset, problem, priority, TicketStatus.OPEN)
        print(f"Created: {ticket}")
    except TicketAlreadyExistsError as e:
        print(f"Error: {e}")

def view_ticket(ticket_service):
    ticket_id = get_valid_id()

    try:
        save = ticket_service.get_ticket(ticket_id)
        print(f"----- Ticket Information {ticket_id} -----")
        print(save)
    except TicketNotFoundError as e:
        print(f"Error: {e}")

def view_all_tickets(ticket_service):
    all_tickets = ticket_service.get_all_tickets()

    print("\n----- All Tickets List -----")
    for item in all_tickets:
        print(item)

def assign_ticket(ticket_service):
    ticket_id = get_valid_id("Please enter Ticket ID: ")
    technician_id = get_valid_id("Please enter Technician ID: ")

    try:
        ticket = ticket_service.assign_technician(ticket_id, technician_id)
        print(f"Ticket({ticket_id}) assigned to technician with ID: {technician_id}. Ticket Status: {ticket.status}")
    except (TicketNotFoundError, TechnicianNotFoundError, TicketNotOpenError) as e:
        print(f"Error: {e}")

def add_comment(ticket_service):
    ticket_id = get_valid_id("Please enter Ticket ID: ")

    text = get_valid_text("Please enter the comment (or 'c' to cancel): ")
    if text is None:
        return

    author_name = get_valid_name("Please enter your name (or 'c' to cancel): ")
    if author_name is None:
        return

    author_role = get_valid_text("Please enter your role (or 'c' to cancel): ")
    if author_role is None:
        return

    try:
        ticket = ticket_service.add_comment(ticket_id, text, author_name, author_role)
        print(f"Comment added to ticket {ticket_id}.")
        print(ticket)
    except (TicketNotFoundError, CommentEmptyError, TicketClosedError) as e:
        print(f"Error: {e}")

def resolve_ticket(ticket_service):
    ticket_id = get_valid_id("Please enter Ticket ID: ")
    technician_id = get_valid_id("Please enter Technician ID: ")

    try:
        ticket = ticket_service.resolve_ticket(ticket_id, technician_id)
        print(f"Ticket({ticket_id}) resolved by technician {technician_id}. Ticket Status: {ticket.status}")
    except (TicketNotFoundError, TechnicianNotFoundError, TicketNotInProgressError, TechnicianNotAssignedError) as e:
        print(f"Error: {e}")

def confirm_resolution(ticket_service):
    ticket_id = get_valid_id("Please enter Ticket ID: ")
    employee_id = get_valid_id("Please enter Employee ID: ")

    is_fixed = get_valid_yes_no("Is the problem fixed? (yes/no, or 'c' to cancel): ")
    if is_fixed is None:
        return

    if is_fixed:
        comment = input("Comment (optional): ")
    else:
        comment = get_valid_text("Please summarize what is still wrong (or 'c' to cancel): ")
        if comment is None:
            return

    try:
        ticket = ticket_service.confirm_resolution(ticket_id, employee_id, is_fixed, comment)

        if is_fixed:
            print(f"Ticket({ticket_id}) confirmed as fixed. Ticket Status: {ticket.status}. "
                  f"The technician can now close it.")
        else:
            print(f"Ticket({ticket_id}) sent back to technician "
                  f"{ticket.technician.technician_id}. Ticket Status: {ticket.status}")
    except (TicketNotFoundError, TicketNotResolvedError, EmployeeNotTicketOwnerError,
            TicketAlreadyConfirmedError, CommentEmptyError) as e:
        print(f"Error: {e}")

def close_ticket(ticket_service):
    ticket_id = get_valid_id("Please enter Ticket ID: ")
    technician_id = get_valid_id("Please enter Technician ID: ")

    try:
        ticket = ticket_service.close_ticket(ticket_id, technician_id)
        print(f"Ticket ID: {ticket.ticket_id} is closed completely. - "
              f"Ticket Status: {ticket.status}")

    except (TicketNotFoundError, TicketNotResolvedError,
            TechnicianNotAssignedError, TechnicianNotFoundError, TicketNotConfirmedError) as e:
        print(f"Error: {e}")
        