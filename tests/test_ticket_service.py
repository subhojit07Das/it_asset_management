import pytest
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService
from app.repositories.technician_repository import TechnicianRepository 
from app.services.technician_service import TechnicianService 
from app.utils.enums import TicketPriority, TicketStatus
from app.exceptions.ticket_exceptions import TicketAlreadyExistsError, TicketNotFoundError, TicketNotOpenError
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