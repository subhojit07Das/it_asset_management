from app.services.employee_service import EmployeeService
from app.repositories.employee_repository import EmployeeRepository
from app.services.asset_service import AssetService
from app.repositories.asset_repository import AssetRepository
from app.services.technician_service import TechnicianService
from app.repositories.technician_repository import TechnicianRepository
from app.services.ticket_service import TicketService
from app.repositories.ticket_repository import TicketRepository
from app.services.assignment_service import AssignmentService
from cli.menu.menu import main_menu

employee = EmployeeRepository()
employee_service = EmployeeService(employee)
ser1 = AssetRepository()
asset_service = AssetService(ser1)
tech_serv = TechnicianRepository()
technician_service = TechnicianService(tech_serv)   
ticket_repo = TicketRepository()             
tick_service = TicketService(technician_service, ticket_repo)  
assignment_service = AssignmentService(employee_service, asset_service)

main_menu(employee_service, asset_service, technician_service, tick_service, assignment_service)