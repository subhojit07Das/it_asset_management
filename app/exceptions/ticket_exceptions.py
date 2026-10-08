class TicketNotFoundError(Exception):
    pass

class TicketNotOpenError(Exception):
    pass

class TicketAlreadyExistsError(Exception):
    pass

class CommentEmptyError(Exception):
    pass

class TicketClosedError(Exception):
    pass

class TicketNotInProgressError(Exception):
    pass

class TechnicianNotAssignedError(Exception):
    pass

class TicketNotResolvedError(Exception):
    pass

class TicketNotConfirmedError(Exception):
    pass

class EmployeeNotTicketOwnerError(Exception):
    pass

class TicketAlreadyConfirmedError(Exception):
    pass