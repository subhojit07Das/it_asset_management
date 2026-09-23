# IT Asset & Ticket Management System

A Python-based IT Asset and Ticket Management System built to practice **Object-Oriented Programming (OOP)** and clean project structure.

The project is initially being developed as a **CLI application**. Later, the same core business logic will be extended with a database, FastAPI, Docker, and CI/CD.

## Project Goals

This project is designed to practice:

* Object-Oriented Programming
* Classes and objects
* Encapsulation
* Inheritance
* Polymorphism
* Abstraction
* Composition
* Exception handling
* Type hints
* Separation of concerns
* Repository pattern
* Service layer
* Unit testing

## Current Scope

The initial version is a CLI application.

The system will manage:

* Employees
* IT assets
* Asset assignments
* Technicians
* Support tickets
* Ticket status
* Ticket priority
* Ticket comments
* Asset lifecycle

## Planned Architecture

```text
CLI
 │
 ▼
Services
 │
 ▼
Models
 │
 ▼
Repositories
 │
 ▼
In-memory storage
```

The initial version does **not** use:

* FastAPI
* Database
* Docker
* CI/CD

These will be introduced in later stages.

## Project Structure

```text
it_asset_management/
│
├── app/
│   ├── __init__.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── employee.py
│   │   ├── asset.py
│   │   ├── laptop.py
│   │   ├── monitor.py
│   │   └── phone.py
│   │
│   ├── services/
│   │   └── __init__.py
│   │
│   ├── repositories/
│   │   └── __init__.py
│   │
│   ├── exceptions/
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── enums.py
│
├── tests/
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Current Progress

### Phase 1 — Python OOP Foundation ✅

The core OOP foundation has been implemented.

Completed:

* Employee model
* Base Asset model
* Asset type and status enums
* Laptop model using inheritance
* Monitor model using inheritance
* Phone model using inheritance
* `super()` for parent class initialization
* Type hints
* Employee-to-asset assignment
* Multiple assets assigned to an employee
* Separate asset collections for different employees

Current object relationship:

```text
Employee
 │
 └── assigned_assets
        ├── Laptop
        ├── Monitor
        └── Phone
```

### Phase 2 — Business Logic 🚧

The next stage will introduce service classes responsible for application operations such as:

* Employee management
* Asset management
* Asset assignment
* Asset status management

### Phase 3 — Repository Layer

Implement in-memory repositories for:

* Employees
* Assets
* Tickets

### Phase 4 — Custom Exceptions

Add application-specific exceptions for:

* Invalid operations
* Missing resources
* Invalid asset assignments
* Other business-rule violations

### Phase 5 — CLI

Create a command-line interface for interacting with the system.

Planned functionality:

* Create employees
* Create assets
* Assign assets to employees
* View employees
* View assets
* View assets assigned to an employee
* Manage asset status
* Handle invalid operations

### Phase 6 — Testing

Add unit tests using `pytest`.

## Future Phases

After the CLI version is stable:

1. Database / PostgreSQL integration
2. FastAPI API layer
3. Docker
4. CI/CD with GitHub Actions
5. Deployment
6. Logging and monitoring

## Development Philosophy

The project is being developed incrementally.

The primary goal is to understand and implement the underlying Python and OOP concepts before introducing frameworks and infrastructure.

FastAPI, databases, Docker, and CI/CD will be added only after the core CLI application is working correctly.

## Status

**Current stage:** Python OOP foundation completed ✅

**Next stage:** Business logic and service layer 🚧
