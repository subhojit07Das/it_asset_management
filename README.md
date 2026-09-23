# IT Asset & Ticket Management System

A Python-based IT Asset and Ticket Management System built to practice **Object-Oriented Programming (OOP)** and clean project structure.

The project will initially be developed as a **CLI application**. Later, the same core business logic can be extended with FastAPI, a database, Docker, and CI/CD.

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

The initial version will be a CLI application.

The system will eventually manage:

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

The initial version will **not** use:

* FastAPI
* Database
* Docker
* CI/CD

These will be considered in later stages.

## Project Structure

```text
it_asset_management/
│
├── app/
│   ├── __init__.py
│   │
│   ├── models/
│   │   └── __init__.py
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
│       └── __init__.py
│
├── tests/
│   └── __init__.py
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Development Roadmap

### Phase 1 — OOP Models

Create and develop the core domain models:

* Employee
* Technician
* Asset
* Laptop
* Monitor
* Phone
* Ticket
* Comment

### Phase 2 — Business Logic

Create service classes responsible for operations such as:

* Employee management
* Asset management
* Asset assignment
* Ticket creation
* Ticket assignment
* Ticket status management

### Phase 3 — Repository Layer

Implement in-memory repositories for:

* Employees
* Assets
* Tickets

### Phase 4 — Custom Exceptions

Add application-specific exceptions for invalid operations and missing resources.

### Phase 5 — CLI

Create a command-line interface for interacting with the system.

### Phase 6 — Testing

Add unit tests using `pytest`.

### Future Phases

After the CLI version is stable:

1. Database integration
2. FastAPI API layer
3. Docker
4. CI/CD
5. Deployment

## Development Philosophy

The project is being developed incrementally.

The primary goal is to understand and implement the underlying Python and OOP concepts before introducing frameworks and infrastructure.

FastAPI, databases, Docker, and CI/CD will be added only after the core CLI application is working correctly.

## Status

**Current stage:** Initial project structure

The next stage is to design and implement the core OOP models.
