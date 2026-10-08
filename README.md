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
* Automated unit tests with pytest (51 tests)
* Interactive command-line interface (CLI) with a menu per area
* Ticket comments (text, author, role, timestamp)
* Full ticket lifecycle: open → in progress → resolved → confirmed by the employee → closed, with a way back to in progress
* Git feature-branch workflow

### Planned

* Unassign a technician from a ticket
* Automatic ending for tickets the employee never answers
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
CLI (menus and input validation)
       ↓
Service Layer        → business rules and validation
       ↓
Repository Layer     → data storage (in-memory for now)
       ↓
Domain Models        → Employee, Asset, Ticket, Comment, ...
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
Comment
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

### Where responsibilities live

* **CLI:** asks for input, validates its format (numbers, non-empty text, valid enum values), calls a service, and prints the result or the error.
* **Services:** own all business rules (can this asset be assigned? can this ticket be resolved?) and raise domain exceptions when a rule is broken.
* **Models:** hold data and simple behaviour (for example, a ticket prints its comments one per line).

Because the rules live in the services, a future FastAPI layer can reuse them without any change.

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
│   │   ├── comment.py
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
├── cli/
│   ├── helpers/
│   │   └── input_helper.py
│   │
│   └── menu/
│       ├── menu.py
│       ├── employee_menu.py
│       ├── asset_menu.py
│       ├── technician_menu.py
│       ├── ticket_menu.py
│       └── assignment_menu.py
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
* A confirmation flag, set when the employee confirms the fix

### Comment

* Text, author name, author role
* A timestamp that the comment sets itself when it is created

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

### Ticket Lifecycle

```text
OPEN
  ↓  technician assigned
IN_PROGRESS  ◄───────────────────────────┐
  ↓  assigned technician resolves        │  employee answers "no, still broken"
RESOLVED ────────────────────────────────┘
  ↓  employee answers "yes, it is fixed"
RESOLVED (confirmed)
  ↓  assigned technician closes the ticket
CLOSED
```

The technician cannot close a ticket on their own. The employee who raised it has to confirm the fix first. If the employee says it is not fixed, the ticket goes back to `IN_PROGRESS` with the same technician, and the cycle repeats.

| Action | Allowed when | Otherwise |
|--------|--------------|-----------|
| Assign technician | Ticket exists, technician exists, ticket is `OPEN` | `TicketNotFoundError`, `TechnicianNotFoundError`, `TicketNotOpenError` |
| Resolve ticket | Ticket is `IN_PROGRESS` **and** the person resolving it is the assigned technician | `TicketNotFoundError`, `TicketNotInProgressError`, `TechnicianNotAssignedError` |
| Confirm resolution | Ticket is `RESOLVED`, the person answering is the employee who raised it, and it is not already confirmed. A "no" must come with a comment; a "yes" may | `TicketNotFoundError`, `TicketNotResolvedError`, `EmployeeNotTicketOwnerError`, `TicketAlreadyConfirmedError`, `CommentEmptyError` |
| Close ticket | Ticket is `RESOLVED`, the person closing it is the assigned technician, **and** the employee has confirmed | `TicketNotFoundError`, `TicketNotResolvedError`, `TechnicianNotAssignedError`, `TicketNotConfirmedError` |
| Add comment | Ticket exists, text is not empty (after trimming spaces), ticket is not `CLOSED` | `TicketNotFoundError`, `CommentEmptyError`, `TicketClosedError` |

* **Answer "yes":** the ticket is marked as confirmed and stays `RESOLVED` until the technician closes it.
* **Answer "no":** the status returns to `IN_PROGRESS`, the technician stays assigned, and the employee's comment explains what is still wrong.
* **Employee comments** are filled in automatically from the ticket's employee, with the role "Employee", so nobody types a role by hand.

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
├── TicketAlreadyExistsError
├── TicketNotOpenError
├── TicketNotInProgressError
├── TicketClosedError
├── TechnicianNotAssignedError
├── TicketNotResolvedError
├── TicketNotConfirmedError
├── TicketAlreadyConfirmedError
├── EmployeeNotTicketOwnerError
└── CommentEmptyError
```

General flow:

```text
Service checks a business rule
        ↓
Rule violated
        ↓
Domain-specific exception raised
        ↓
Calling layer (CLI / future API) decides how to present the error
```

In the CLI, every menu action catches exactly the exceptions its service method can raise and prints a readable `Error: ...` message, so a bad ID or a broken rule returns the user to the menu instead of crashing the program.

---

## Command-Line Interface

`main.py` creates the repositories and services, wires them together, and starts the CLI.

```text
=== IT Asset Management System ===
1. Employee Menu
2. Asset Menu
3. Technician Menu
4. Ticket Menu
5. Assignment Menu
6. Exit
```

| Menu | Options |
|------|---------|
| Employee | Create, View, View All, Delete |
| Asset | Create, View, View All, Delete |
| Technician | Create, View, View All, Delete |
| Ticket | Create, View, View All, Assign technician, Add comment, Resolve, Confirm resolution, Close |
| Assignment | Assign asset to employee, Unassign asset from employee |

### Input handling

Shared helpers in `cli/helpers/input_helper.py` keep asking until the input is valid:

* IDs must be numbers
* Text fields cannot be empty
* Asset type, asset status, and ticket priority must be valid enum values (case-insensitive)
* Yes/no questions accept `yes` or `no`
* Typing `c` cancels the prompts that offer it

### Example session

```text
----- Ticket Menu -----
Choose an option: 4
Please enter ticket ID: 1
Please enter technician ID: 100
Ticket(1) assigned to technician with ID: 100. Ticket Status: In Progress

Choose an option: 5
Please enter ticket ID: 1
Please enter the comment: Display issue
Please enter your name: tech1
Please enter your role: IT Support
Comment added to ticket 1.

Choose an option: 2
----- Ticket Information 1 -----
Ticket(1) - Employee: ... - Status: In Progress - Technician: Technician(100) - ...
Comments:
[2026-10-07 12:26] TECH1 (IT Support): Display issue

Choose an option: 6
Please enter Ticket ID: 1
Please enter Technician ID: 100
Ticket(1) resolved by technician 100. Ticket Status: Resolved

Choose an option: 7
Please enter Ticket ID: 1
Please enter Employee ID: 1
Is the problem fixed? (yes/no, or 'c' to cancel): yes
Comment (optional): Works now
Ticket(1) confirmed as fixed. Ticket Status: Resolved. The technician can now close it.

Choose an option: 8
Please enter Ticket ID: 1
Please enter Technician ID: 100
Ticket ID: 1 is closed completely. - Ticket Status: Closed
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
└── test_ticket_service.py       (28 tests)
                                 ────────
                                 51 tests
```

### What is tested

* **Employees / Technicians / Assets:** creation, duplicate-ID rejection, lookup of missing IDs, deletion of missing IDs, existence checks, and listing all records (`get_all_*`)
* **Asset types:** creation of each specialized asset type (Laptop, Monitor, Phone), including the Phone-specific fields
* **Assignment:** successful assignment, assigning an unavailable asset, assigning to a missing employee, assigning a missing asset, unassigning an asset that is not assigned, unassigning an asset belonging to a different employee
* **Tickets:** creation, duplicate-ID rejection, listing all tickets, technician assignment (success, non-open ticket, missing ticket, missing technician)
* **Ticket comments:** adding a comment (with surrounding spaces trimmed), missing ticket, empty text, closed ticket
* **Resolving tickets:** success, missing ticket, ticket not in progress, and a technician who is not the one assigned
* **Confirming the fix:** "yes" with and without a comment, "no" with a comment (ticket returns to in progress, same technician), "no" without a comment, a ticket that is not resolved, a missing ticket, an employee who does not own the ticket, and answering twice
* **Closing tickets:** success, ticket not resolved, wrong technician, and a ticket the employee has not confirmed
* **Full flow:** assign → resolve → "no" → resolve again → "yes" → close, checked step by step

### Testing approach

* **Fixtures** build a fresh repository and service for every test, so tests never share state.
* Fixtures are chained (repository → service → assignment service), mirroring the dependency injection used in the application.
* `pytest.raises` verifies that the correct exception is raised for each business-rule violation.
* Error tests set up everything else correctly, so the exception being tested is the only one that can occur.

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

### Run the application

```bash
python main.py
```

This starts the interactive menu. All data is kept in memory, so it is lost when the program exits (a database is planned).

### Run the tests

```bash
python -m pytest
```

Useful options:

```bash
python -m pytest -v                              # verbose output
python -m pytest tests/test_ticket_service.py    # a single test file
python -m pytest -k resolve                      # only tests with "resolve" in the name
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
feature/testing
feature/cli
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
6. CLI                             ✅
      ↓
7. Ticket workflow (comments,      ✅ comments, resolve, confirm, close
   resolve, confirm, close,        ⏳ unassign
   unassign)
      ↓
8. PostgreSQL                      ← NEXT
      ↓
9. FastAPI
      ↓
10. Docker
      ↓
11. CI/CD
      ↓
12. Deployment
      ↓
13. Logging & Monitoring
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
* A command-line interface on top of the service layer
* PostgreSQL integration
* REST API development
* Containerization
* CI/CD
* Deployment
* Logging and monitoring
* Git-based development workflow