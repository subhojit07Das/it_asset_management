from app.models.technician import Technician

class Ticket:
    def __init__(self, ticket_id, employee, asset, problem, priority, status):
        self.ticket_id = ticket_id
        self.employee = employee
        self.asset = asset
        self.problem = problem
        self.priority = priority
        self.status = status
        self.technician = None
        self.comments = []

    def __str__(self):
        return f"Ticket ID: {self.ticket_id} \nEmployee: {self.employee} \nAsset: {self.asset} \nProblem: {self.problem} \nPriority: {self.priority} \nStatus: {self.status} \nTechnician: {self.technician} \nComments: {self.comments}"

    def add_technician(self, technician: Technician):
        self.technician =  technician