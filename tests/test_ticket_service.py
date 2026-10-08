import pytest
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService
from app.repositories.technician_repository import TechnicianRepository 
from app.services.technician_service import TechnicianService 
from app.utils.enums import TicketPriority, TicketStatus
from app.exceptions.ticket_exceptions import (
    TicketAlreadyExistsError, TicketNotFoundError, TicketNotOpenError, TicketClosedError, CommentEmptyError, TicketNotInProgressError, TechnicianNotAssignedError, TicketAlreadyConfirmedError, TicketNotConfirmedError, EmployeeNotTicketOwnerError, TicketNotResolvedError)
from app.exceptions.technician_exceptions import TechnicianNotFoundError
from app.models.employee import Employee

@pytest.fixture
def employee():
    return Employee(200, "Alice", "alice@mail.com", "Finance")

@pytest.fixture
def ticket_repo():
    return TicketRepository()

@pytest.fixture
def technician_repo():
    return TechnicianRepository()

@pytest.fixture
def technician_service(technician_repo):
    return TechnicianService(technician_repo)

@pytest.fixture
def ticket_service(technician_service, ticket_repo):
    return TicketService(technician_service, ticket_repo)

def test_create_ticket(ticket_service, ticket_repo):
    ticket = ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    assert ticket.ticket_id == 1
    assert ticket.problem == "Laptop won't boot"
    assert ticket.priority == TicketPriority.HIGH
    assert ticket.status == TicketStatus.OPEN
    assert ticket_repo.exists(1)

def test_create_ticket_duplicate_id_raise(ticket_service):
    ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    with pytest.raises(TicketAlreadyExistsError):
        ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

def test_assign_technician_success(technician_service, ticket_service):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)

    assert ticket.status == TicketStatus.IN_PROGRESS
    assert ticket.technician == technician

def test_assign_technician_ticket_not_open_raises(technician_service, ticket_service):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")
    
    ticket = ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)

    assert ticket.status == TicketStatus.IN_PROGRESS

    with pytest.raises(TicketNotOpenError):
        ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)

def test_assign_technician_missing_ticket_raises(technician_service, ticket_service):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    with pytest.raises(TicketNotFoundError):
        ticket_service.assign_technician(999, technician.technician_id)

def test_assign_technician_missing_technician_raises(ticket_service):
    ticket = ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    with pytest.raises(TechnicianNotFoundError):
        ticket_service.assign_technician(ticket.ticket_id, 999)

def test_get_all_tickets(ticket_service):
    ticket = ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket2 = ticket_service.create_ticket(2, "employee_placeholder", "asset_placeholder", "Mobile won't start", TicketPriority.LOW, TicketStatus.OPEN)

    all_tickets = list(ticket_service.get_all_tickets())

    assert len(all_tickets) == 2
    assert ticket in all_tickets
    assert ticket2 in all_tickets

def test_add_comment(ticket_service):
    ticket = ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    result = ticket_service.add_comment(1, "  hello  ", "Aizen", "technician_role")

    assert len(result.comments) == 1
    assert result.comments[0].text == "hello"
    assert result.comments[0].author_name == "Aizen"

def test_add_comment_missing_ticket_raises(ticket_service):
    with pytest.raises(TicketNotFoundError):
        ticket_service.add_comment(999, "hello", "Aizen", "technician_role")

def test_add_comment_empty_text_raises(ticket_service):
    ticket = ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    with pytest.raises(CommentEmptyError):
        ticket_service.add_comment(1, "   ", "Aizen", "technician_role")

    assert len(ticket.comments) == 0

def test_add_comment_closed_ticket_raises(ticket_service):
    ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.CLOSED)

    with pytest.raises(TicketClosedError):
        ticket_service.add_comment(1, "hello", "Aizen", "technician_role")

def test_resolve_ticket(ticket_service, technician_service):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)
    result = ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)

    assert result.status == TicketStatus.RESOLVED
    assert ticket.technician == technician

def test_resolve_ticket_missing_ticket_raises(ticket_service):
    with pytest.raises(TicketNotFoundError):
        ticket_service.resolve_ticket(999, 999)

def test_resolve_ticket_not_in_progress_raises(ticket_service, technician_service):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    with pytest.raises(TicketNotInProgressError):
        ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)

def test_resolve_ticket_wrong_technician_raises(ticket_service, technician_service):
    technician1 = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    technician2 = technician_service.create_technician(101, "Tech2", "tech2@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, "employee_placeholder", "asset_placeholder", "Laptop won't boot", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician1.technician_id)
    
    with pytest.raises(TechnicianNotAssignedError):
        ticket_service.resolve_ticket(ticket.ticket_id, technician2.technician_id)

def test_close_ticket(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)
    ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)
    ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, True, "Fixed")

    result = ticket_service.close_ticket(ticket.ticket_id, technician.technician_id)

    assert result.status == TicketStatus.CLOSED

def test_close_ticket_not_resolved(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)

    with pytest.raises(TicketNotResolvedError):
        ticket_service.close_ticket(ticket.ticket_id, technician.technician_id)

    assert ticket.status == TicketStatus.IN_PROGRESS

def test_close_ticket_wrong_technician_raise(ticket_service, technician_service, employee):
    technician1 = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    technician2 = technician_service.create_technician(101, "Tech2", "tech2@mail.com", "IT Support1")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician1.technician_id)
    ticket_service.resolve_ticket(ticket.ticket_id, technician1.technician_id)
    ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, True, "Fixed")

    with pytest.raises(TechnicianNotAssignedError):
        ticket_service.close_ticket(ticket.ticket_id, technician2.technician_id)

def test_close_ticket_not_confirmed(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)
    ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)

    with pytest.raises(TicketNotConfirmedError):
        ticket_service.close_ticket(ticket.ticket_id, technician.technician_id)

    assert ticket.status == TicketStatus.RESOLVED

def test_confirm_resolution_yes_with_comment(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)
    ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)

    result = ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, True, "Fixed")

    assert result.confirmed is True
    assert result.status == TicketStatus.RESOLVED
    assert len(result.comments) == 1
    assert result.comments[0].text == "Fixed"
    assert result.comments[0].author_name == "Alice"
    assert result.comments[0].author_role == "Employee"

def test_confirm_resolution_wrong_employee_raises(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)
    ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)

    with pytest.raises(EmployeeNotTicketOwnerError):
        ticket_service.confirm_resolution(ticket.ticket_id, 201, True, "Fixed")
 
    assert len(ticket.comments) == 0
    assert ticket.confirmed is False
    assert ticket.status == TicketStatus.RESOLVED

def test_confirm_resolution_already_confirmed_raises(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)
    ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)

    result = ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, True, "Fixed")

    with pytest.raises(TicketAlreadyConfirmedError):
        ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, True, "Fixed")

    assert result.confirmed is True
    assert result.status == TicketStatus.RESOLVED
    assert len(result.comments) == 1

def test_confirm_resolution_missing_ticket_raises(ticket_service):
    with pytest.raises(TicketNotFoundError):
        ticket_service.confirm_resolution(999, 200, True, "Fixed")

def test_confirm_resolution_no_with_comment(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)
    ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)

    result = ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, False, "Still Broken")

    assert result.confirmed is False
    assert result.status == TicketStatus.IN_PROGRESS
    assert len(result.comments) == 1
    assert result.technician == technician

def test_confirm_resolution_no_empty_comment_raises(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)
    ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)

    with pytest.raises(CommentEmptyError):
        ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, False, "   ")

    assert ticket.status == TicketStatus.RESOLVED
    assert ticket.confirmed is False
    assert len(ticket.comments) == 0

def test_confirm_resolution_yes_without_comment(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)
    ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)

    result = ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, True, "")

    assert result.confirmed is True
    assert result.status == TicketStatus.RESOLVED
    assert len(result.comments) == 0

def test_confirm_resolution_not_resolved_raises(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)

    with pytest.raises(TicketNotResolvedError):
        ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, True, "")

    assert ticket.status == TicketStatus.IN_PROGRESS
    assert ticket.confirmed is False

def test_full_flow_no_then_yes_then_close(ticket_service, technician_service, employee):
    technician = technician_service.create_technician(100, "Tech1", "tech1@mail.com", "IT Support")

    ticket = ticket_service.create_ticket(1, employee, "asset_placeholder", "Laptop not working", TicketPriority.HIGH, TicketStatus.OPEN)

    # assign and resolve
    ticket_service.assign_technician(ticket.ticket_id, technician.technician_id)
    ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)
    assert ticket.status == TicketStatus.RESOLVED

    # employee comment "no"
    ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, False, "Not yet fixed")
    assert ticket.status == TicketStatus.IN_PROGRESS
    assert ticket.confirmed is False
    assert ticket.technician == technician

    # technician resolve again
    ticket_service.resolve_ticket(ticket.ticket_id, technician.technician_id)
    assert ticket.status == TicketStatus.RESOLVED

    # employee comment "yes"
    ticket_service.confirm_resolution(ticket.ticket_id, employee.employee_id, True, "Fixed")
    assert ticket.status == TicketStatus.RESOLVED
    assert ticket.confirmed is True

    # technician closes
    ticket_service.close_ticket(ticket.ticket_id, technician.technician_id)
    assert ticket.status == TicketStatus.CLOSED
    assert len(ticket.comments) == 2
    