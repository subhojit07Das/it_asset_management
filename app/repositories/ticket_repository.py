from app.models.ticket import Ticket

class TicketRepository:
    def __init__(self):
        self.tickets = {}

    def save(self, ticket: Ticket):
        self.tickets[ticket.ticket_id] = ticket
        return ticket

    def get_by_id(self, ticket_id):
        return self.tickets.get(ticket_id)

    def get_all(self):
        return self.tickets.values()

    def delete(self, ticket_id):
        if ticket_id in self.tickets:
            del self.tickets[ticket_id]
            return True
        
        return False

    def exists(self, ticket_id):
        return ticket_id in self.tickets