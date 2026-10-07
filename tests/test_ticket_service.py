import pytest
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService
from app.repositories.technician_repository import TechnicianRepository 
from app.services.technician_service import TechnicianService 
from app.utils.enums import TicketPriority, TicketStatus
from app.exceptions.ticket_exceptions import TicketAlreadyExistsError, TicketNotFoundError, TicketNotOpenError, TicketClosedError, CommentEmptyError, TicketNotInProgressError, TechnicianNotAssignedError
from app.exceptions.technician_exceptions import TechnicianNotFoundError

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
