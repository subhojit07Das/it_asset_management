from app.utils.enums import TicketStatus
from app.repositories.ticket_repository import TicketRepository
from app.models.ticket import Ticket
from app.exceptions.ticket_exceptions import TicketNotFoundError, TicketNotOpenError, TicketAlreadyExistsError, CommentEmptyError, TicketClosedError, TicketNotInProgressError, TechnicianNotAssignedError
from app.models.comment import Comment

class TicketService:
    def __init__(self, technician_service, tickets: TicketRepository):
        self.technician_service = technician_service
        self.tickets = tickets

    def create_ticket(self, ticket_id, employee, asset, problem, priority, status):
        if self.tickets.exists(ticket_id):
            raise TicketAlreadyExistsError(f"Ticket ID: {ticket_id} already exists.")
        
        ticket = Ticket(ticket_id, employee, asset, problem, priority, status)

        self.tickets.save(ticket)
        return ticket

    def get_ticket(self, ticket_id):
        ticket = self.tickets.get_by_id(ticket_id)

        if ticket is None:
            raise TicketNotFoundError(f"Ticket ID: {ticket_id} not present.")

        return ticket

    def get_all_tickets(self):
        return self.tickets.get_all()

    def assign_technician(self, ticket_id, technician_id):
        ticket = self.get_ticket(ticket_id)
        technician = self.technician_service.get_technician(technician_id)

        if ticket.status != TicketStatus.OPEN:
            raise TicketNotOpenError(f"Ticket ID: {ticket_id} is not open.")

        ticket.add_technician(technician)
        ticket.status = TicketStatus.IN_PROGRESS
        return ticket

    def add_comment(self, ticket_id, text, author_name, author_role):
        ticket = self.get_ticket(ticket_id)
        text = text.strip()

        if not text:
            raise CommentEmptyError(f"Cannot add an empty comment to ticket ID: {ticket_id}.")

        if ticket.status == TicketStatus.CLOSED:
            raise TicketClosedError(f"Ticket ID: {ticket_id} is closed.")

        comment = Comment(text, author_name, author_role)
        ticket.add_comment(comment)

        return ticket

    def resolve_ticket(self, ticket_id, technician_id):
        ticket = self.get_ticket(ticket_id)
        technician = self.technician_service.get_technician(technician_id)

        if ticket.status != TicketStatus.IN_PROGRESS:
            raise TicketNotInProgressError(f"Ticket ID: {ticket_id} is not in progress")

        if ticket.technician.technician_id != technician_id:
            raise TechnicianNotAssignedError(f"Technician ID: {technician_id} is not assigned for Ticket ID: {ticket_id} ")

        ticket.status = TicketStatus.RESOLVED

        return ticket