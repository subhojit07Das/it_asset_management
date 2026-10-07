from app.models.technician import Technician
from app.models.comment import Comment

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
        header = (f"Ticket({self.ticket_id}) - Employee: {self.employee} - Asset: {self.asset} - "
                f"Problem: {self.problem} - Priority: {self.priority} - Status: {self.status} - "
                f"Technician: {self.technician}")

        if not self.comments:
            return f"{header}\nComments: None"

        lines = "\n".join(f"{comment}" for comment in self.comments)
        return f"{header}\nComments:\n{lines}"

    def add_technician(self, technician: Technician):
        self.technician = technician

    def add_comment(self, comment: Comment):
        self.comments.append(comment)