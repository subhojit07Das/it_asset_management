# IT Asset & Ticket Management System

A Python-based IT Asset & Ticket Management System built as a learning and portfolio project.

The project is being developed incrementally, starting with Python OOP and gradually evolving into a complete backend system with a database, REST API, Docker, CI/CD, and deployment.

---

## Current Status

### Completed

* Python OOP-based domain models
* Employee management model
* Asset management model
* Specialized asset types:

  * Laptop
  * Monitor
  * Phone
* Technician model
* Ticket model
* Enum-based asset types and statuses
* Enum-based ticket priorities and statuses
* Employee service layer
* Asset service layer
* Asset assignment service
* Technician service layer
* Ticket service layer
* In-memory repository layer
* Repository integration with service layer
* Dependency injection between services and repositories
* Business-rule validation
* Custom domain-specific exceptions
* Exception handling for Employee operations
* Exception handling for Asset operations
* Exception handling for Technician operations
* Exception handling for Asset Assignment operations
* Exception handling for Ticket operations
* Git feature-branch workflow

### Currently Working On

* CLI interface

### Planned

* Complete CLI functionality
* Automated testing
* PostgreSQL database
* FastAPI REST API
* Docker
* CI/CD pipeline
* Deployment
* Logging and monitoring

---

## Project Architecture

The application currently follows a layered architecture:

```text
CLI / Application
       ↓
Service Layer
       ↓
Repository Layer
       ↓
Domain Models
```

### Models

The model layer represents the core entities of the system.

Current models:

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

The service layer contains application and business logic.

Current services:

```text
EmployeeService
AssetService
AssignmentService
TechnicianService
TicketService
```

### Repositories

The repository layer currently provides in-memory data storage using Python dictionaries.

```text
EmployeeRepository
AssetRepository
TechnicianRepository
TicketRepository
```

The service layer receives repository objects through dependency injection instead of directly creating repositories.

This keeps business logic separated from the data-storage implementation and will make it easier to replace the in-memory repositories with PostgreSQL later.

### Exceptions

The exception layer contains custom domain-specific exceptions used by the service layer.

The current exception categories include:

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

These exceptions allow the service layer to communicate specific business-rule failures instead of relying on generic `None` return values.

---

## Project Structure

```text
it_asset_management/
│
├── app/
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── employee_exceptions.py
│   │   ├── asset_exceptions.py
│   │   ├── technician_exceptions.py
│   │   ├── assignment_exceptions.py
│   │   └── ticket_exceptions.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── asset.py
│   │   ├── employee.py
│   │   ├── laptop.py
│   │   ├── monitor.py
│   │   ├── phone.py
│   │   ├── technician.py
│   │   └── ticket.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── employee_repository.py
│   │   ├── asset_repository.py
│   │   ├── technician_repository.py
│   │   └── ticket_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── employee_service.py
│   │   ├── asset_service.py
│   │   ├── assignment_service.py
│   │   ├── technician_service.py
│   │   └── ticket_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── enums.py
│
├── tests/
│
├── main.py
├── README.md
└── requirements.txt
```

---

## Core Domain

### Employee

An employee contains:

* Employee ID
* Name
* Email
* Department
* Assigned assets

Employees can have asset objects assigned to them.

---

### Asset

The base `Asset` model contains common asset information:

* Asset ID
* Asset type
* Brand
* Model
* Serial number
* Status

Specialized asset classes inherit from the base `Asset` class.

### Laptop

Additional properties:

* RAM
* Storage
* Operating system

### Monitor

Additional properties:

* Resolution
* Screen size
* Refresh rate

### Phone

Additional properties:

* RAM
* Storage
* Operating system
* Battery
* Processor
* Network

---

### Technician

A technician contains:

* Technician ID
* Name
* Email
* Department

Technicians can be assigned to support tickets.

---

### Ticket

A ticket contains:

* Ticket ID
* Employee
* Asset
* Problem
* Priority
* Status
* Assigned technician
* Comments

The currently implemented ticket workflow begins with:

```text
OPEN
  ↓
IN_PROGRESS
```

Additional ticket workflow functionality will be implemented as the project develops.

---

## Asset Assignment

The `AssignmentService` manages the relationship between employees and assets.

Current rules include:

```text
AVAILABLE → Can be assigned
ASSIGNED  → Cannot be assigned again
REPAIR    → Cannot be assigned
RETIRED   → Cannot be assigned
```

An asset can only be unassigned when it is currently assigned and belongs to the specified employee.

When an asset is successfully assigned:

```text
Employee
   ↓
assigned_assets
   ↓
Asset
   ↓
status = ASSIGNED
```

When an asset is successfully unassigned:

```text
Asset
   ↓
status = AVAILABLE
```

Invalid assignment operations raise domain-specific exceptions.

---

## Ticket Management

The current ticket service supports:

* Creating tickets
* Retrieving tickets
* Retrieving all tickets
* Assigning technicians to tickets

Technician assignment follows:

```text
Ticket: OPEN
      +
Technician exists
      ↓
Technician assigned
      ↓
Ticket: IN_PROGRESS
```

The current implementation prevents technician assignment when the ticket is no longer `OPEN`.

Invalid ticket operations raise domain-specific exceptions.

---

## Exception Handling

The project uses custom exceptions to represent domain-specific errors.

Examples include:

```text
EmployeeNotFoundError
EmployeeAlreadyExistsError

AssetNotFoundError
AssetAlreadyExistsError

TechnicianNotFoundError
TechnicianAlreadyExistsError

AssetNotAvailableError
AssetNotAssignedError
AssetNotAssignedToEmployeeError

TicketNotFoundError
TicketNotOpenError
TicketAlreadyExistsError
```

The general flow is:

```text
Repository
    ↓
Service checks business rule
    ↓
Invalid operation
    ↓
Domain-specific exception
    ↓
Application / CLI handles the exception
```

This keeps business-rule validation inside the service layer while allowing the application layer to decide how errors should be presented to the user.

---

## Repository Layer

The repository layer currently uses in-memory dictionaries.

Conceptually:

```text
EmployeeRepository
        ↓
Python Dictionary
        ↓
employee_id → Employee object
```

Each repository currently supports:

* Save
* Get by ID
* Get all
* Delete
* Check existence

The repositories are intentionally simple at this stage.

Later, the repository layer will be adapted to work with PostgreSQL.

---

## Dependency Injection

Services receive their repositories through their constructors.

Conceptually:

```text
Repository
     ↓
Service
     ↓
Business Logic
```

For example:

```text
EmployeeRepository
        ↓
EmployeeService
```

This keeps the service layer independent from the specific storage implementation.

---

## Technologies

### Current

* Python
* Object-Oriented Programming
* Git
* GitHub
* In-memory repositories

### Planned

* Pytest
* PostgreSQL
* FastAPI
* Docker
* GitHub Actions
* Linux
* Deployment platform
* Logging and monitoring tools

---

## Git Workflow

Git is being used throughout the project to practice a realistic development workflow.

Feature/topic branches are created for individual milestones.

Examples:

```text
main
feature/business-logic
feature/asset_service
feature/ticket_service
feature/repository
feature/exceptions
```

Completed feature branches are merged into `main` after testing.

The project will also use Git tags during the Docker/release stage.

### Current Exception Milestone

The custom exception milestone has been implemented and integrated into the service layer.

The latest milestone commit is:

```text
753e30a Add ticket exceptions; enforce in TicketService; update main.py tests
```

---

## Development Roadmap

```text
1. Python OOP
      ↓
2. Business Logic / Services
      ↓
3. Repository Layer
      ↓
4. Custom Exceptions
      ↓
5. CLI                    ← NEXT
      ↓
6. Testing
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

The project intentionally starts with simple in-memory objects and gradually introduces additional layers and technologies.

By the end, the system is intended to demonstrate:

* Python OOP
* Inheritance
* Composition
* Encapsulation
* Service-layer architecture
* Repository pattern
* Dependency injection
* Custom exception handling
* Automated testing
* PostgreSQL integration
* REST API development
* Containerization
* CI/CD
* Deployment
* Logging and monitoring
* Git-based development workflow
