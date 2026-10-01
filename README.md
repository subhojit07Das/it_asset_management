# IT Asset & Ticket Management System

A Python IT Asset & Ticket Management System built as a learning and portfolio project.

The project is being developed incrementally: it starts with Python OOP and a layered architecture, and gradually evolves into a complete backend system with a database, REST API, Docker, CI/CD, and deployment.

---

## Current Status

### Completed

* Python OOP-based domain models
* Specialized asset types (Laptop, Monitor, Phone) using inheritance
* Enum-based asset types/statuses and ticket priorities/statuses
* Service layer for employees, assets, technicians, tickets, and asset assignment
* In-memory repository layer
* Dependency injection between services and repositories
* Business-rule validation
* Custom domain-specific exceptions
* Automated unit tests with pytest (30 tests)
* Git feature-branch workflow

### Planned

* CLI interface
* PostgreSQL database
* FastAPI REST API
* Docker
* CI/CD pipeline (GitHub Actions)
* Deployment
* Logging and monitoring

---

## Project Architecture

The application follows a layered architecture:

```text
Application (main.py demo / future CLI / future API)
       ↓
Service Layer        → business rules and validation
       ↓
Repository Layer     → data storage (in-memory for now)
       ↓
Domain Models        → Employee, Asset, Ticket, ...
```

### Models

```text
Employee
Asset
├── Laptop
├── Monitor
└── Phone
Technician
Ticket
```

### Services

```text
EmployeeService
AssetService
AssignmentService
TechnicianService
TicketService
```

### Repositories

```text
EmployeeRepository
AssetRepository
TechnicianRepository
TicketRepository
```

Each repository stores objects in a Python dictionary (`id → object`) and supports: save, get by ID, get all, delete, and exists.

Services receive their repositories through their constructors (dependency injection) instead of creating them internally. This keeps business logic independent of the storage implementation, so the in-memory repositories can later be replaced with PostgreSQL without rewriting the services.

---

## Project Structure

```text
it_asset_management/
│
├── app/
│   ├── exceptions/
│   │   ├── asset_exceptions.py
│   │   ├── assignment_exceptions.py
│   │   ├── employee_exceptions.py
│   │   ├── technician_exceptions.py
│   │   └── ticket_exceptions.py
│   │
│   ├── models/
│   │   ├── asset.py
│   │   ├── employee.py
│   │   ├── laptop.py
│   │   ├── monitor.py
│   │   ├── phone.py
│   │   ├── technician.py
│   │   └── ticket.py
│   │
│   ├── repositories/
│   │   ├── asset_repository.py
│   │   ├── employee_repository.py
│   │   ├── technician_repository.py
│   │   └── ticket_repository.py
│   │
│   ├── services/
│   │   ├── asset_service.py
│   │   ├── assignment_service.py
│   │   ├── employee_service.py
│   │   ├── technician_service.py
│   │   └── ticket_service.py
│   │
│   └── utils/
│       └── enums.py
│
├── tests/
│   ├── test_asset_service.py
│   ├── test_assignment_service.py
│   ├── test_employee_service.py
│   ├── test_technician_service.py
│   └── test_ticket_service.py
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Core Domain

### Employee

* Employee ID, name, email, department
* A list of assigned assets

### Asset

The base `Asset` class holds the common fields:

* Asset ID, asset type, brand, model, serial number, status

Specialized classes inherit from `Asset` and add their own properties:

| Class | Additional properties |
|-------|----------------------|
| `Laptop` | RAM, storage, operating system |
| `Monitor` | Resolution, screen size, refresh rate |
| `Phone` | RAM, storage, operating system, battery, processor, network |

`AssetService.create_asset()` builds the correct subclass based on the `AssetType` enum.

### Technician

* Technician ID, name, email, department
* Can be assigned to support tickets

### Ticket

* Ticket ID, employee, asset, problem, priority, status
* Assigned technician and a list of comments

---

## Business Rules

### Asset Assignment

`AssignmentService` manages the relationship between employees and assets.

```text
AVAILABLE → can be assigned
ASSIGNED  → cannot be assigned again
REPAIR    → cannot be assigned
RETIRED   → cannot be assigned
```

* Assigning an asset adds it to the employee's `assigned_assets` and sets its status to `ASSIGNED`.
* An asset can only be unassigned if it is currently `ASSIGNED` **and** belongs to the specified employee. Unassigning sets its status back to `AVAILABLE`.

### Ticket Workflow

```text
OPEN  +  technician exists
        ↓
technician assigned
        ↓
IN_PROGRESS
```

Technician assignment is rejected if the ticket does not exist, the technician does not exist, or the ticket is no longer `OPEN`.

The `RESOLVED` and `CLOSED` statuses are defined in the enum; the transitions into them will be added as the workflow is extended.

---

## Exception Handling

Instead of returning `None` or generic errors, the service layer raises domain-specific exceptions:

```text
Employee
├── EmployeeNotFoundError
└── EmployeeAlreadyExistsError

Asset
├── AssetNotFoundError
└── AssetAlreadyExistsError

Technician
├── TechnicianNotFoundError
└── TechnicianAlreadyExistsError

Assignment
├── AssetNotAvailableError
├── AssetNotAssignedError
└── AssetNotAssignedToEmployeeError

Ticket
├── TicketNotFoundError
├── TicketNotOpenError
└── TicketAlreadyExistsError
```

General flow:

```text
Service checks a business rule
        ↓
Rule violated
        ↓
Domain-specific exception raised
        ↓
Calling layer (CLI / API) decides how to present the error
```

---

## Testing

Automated tests are written with **pytest** and cover the service layer, including every custom exception path.

```text
tests/
├── test_asset_service.py        (7 tests)
├── test_assignment_service.py   (6 tests)
├── test_employee_service.py     (4 tests)
├── test_technician_service.py   (6 tests)
└── test_ticket_service.py       (7 tests)
                                 ────────
                                 30 tests
```

### What is tested

* **Employees / Technicians / Assets:** creation, duplicate-ID rejection, lookup of missing IDs, deletion of missing IDs, existence checks, and listing all records (`get_all_*`)
* **Asset types:** creation of each specialized asset type (Laptop, Monitor, Phone), including the Phone-specific fields
* **Assignment:** successful assignment, assigning an unavailable asset, assigning to a missing employee, assigning a missing asset, unassigning an asset that is not assigned, unassigning an asset belonging to a different employee
* **Tickets:** creation, duplicate-ID rejection, listing all tickets, technician assignment success, assignment to a non-open ticket, missing ticket, missing technician

### Testing approach

* **Fixtures** build a fresh repository and service for every test, so tests never share state.
* Fixtures are chained (repository → service → assignment service), mirroring the dependency injection used in the application.
* `pytest.raises` verifies that the correct exception is raised for each business-rule violation.

---

## Getting Started

### Prerequisites

* Python 3.10+
* Git

### Setup

```bash
git clone https://github.com/subhojit07Das/it_asset_management.git
cd it_asset_management

python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### Run the demo script

```bash
python main.py
```

`main.py` is a demonstration script that exercises the services and prints the result of each business-rule check.

### Run the tests

```bash
pytest
```

Useful options:

```bash
pytest -v                                  # verbose output
pytest tests/test_ticket_service.py        # a single test file
```

---

## Technologies

### Current

* Python
* Object-Oriented Programming
* Pytest
* Git & GitHub
* In-memory repositories

### Planned

* PostgreSQL
* FastAPI
* Docker
* GitHub Actions
* Linux
* Deployment platform
* Logging and monitoring tools

---

## Git Workflow

Feature/topic branches are created for individual milestones and merged into `main` after testing.

```text
main
feature/business-logic
feature/asset_service
feature/ticket_service
feature/repository
feature/exceptions
```

Git tags will be used during the Docker/release stage.

---

## Development Roadmap

```text
1. Python OOP                      ✅
      ↓
2. Business Logic / Services       ✅
      ↓
3. Repository Layer                ✅
      ↓
4. Custom Exceptions               ✅
      ↓
5. Automated Testing (pytest)      ✅
      ↓
6. CLI                             ← NEXT
      ↓
7. PostgreSQL
      ↓
8. FastAPI
      ↓
9. Docker
      ↓
10. CI/CD
      ↓
11. Deployment
      ↓
12. Logging & Monitoring
```

---

## Project Goal

The goal of this project is to build the system incrementally while learning how a real-world Python backend application is structured.

By the end, the system is intended to demonstrate:

* Python OOP: inheritance, composition, encapsulation
* Service-layer architecture
* Repository pattern and dependency injection
* Custom exception handling
* Automated testing
* PostgreSQL integration
* REST API development
* Containerization
* CI/CD
* Deployment
* Logging and monitoring
* Git-based development workflow