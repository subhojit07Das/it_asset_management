from app.utils.enums import TicketStatus
from app.models.ticket import Ticket

class TicketService:
    def __init__(self, technician_service):
        self.tickets = {}
        self.technician_service = technician_service

    def create_ticket(self, ticket_id, employee, asset, problem, priority, status):
        ticket = Ticket(ticket_id, employee, asset, problem, priority, status)

        self.tickets[ticket_id] = ticket
        return ticket

    def get_ticket(self, ticket_id):
        return self.tickets.get(ticket_id)

    def get_all_tickets(self):
        return self.tickets.values()

    def assign_technician(self, ticket_id, technician_id):
        ticket = self.get_ticket(ticket_id)
        technician = self.technician_service.get_technician(technician_id)

        if ticket is None or technician is None:
            return None

        if ticket.status != TicketStatus.OPEN:
            return None

        ticket.add_technician(technician)
        ticket.status = TicketStatus.IN_PROGRESS
        return ticket
    