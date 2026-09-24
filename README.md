# IT Asset & Ticket Management System

## Project Overview

The IT Asset & Ticket Management System is a Python-based project designed to manage IT assets, employees, technicians, and support tickets.

The project is being developed incrementally to demonstrate Object-Oriented Programming, business logic, software architecture, testing, database integration, API development, containerization, and CI/CD practices.

## Current Scope

The system currently supports:

* Employee management
* IT asset management
* Specialized asset types:

  * Laptop
  * Monitor
  * Phone
* Asset status management:

  * Available
  * Assigned
  * Repair
  * Retired
* Assigning assets to employees
* Unassigning assets from employees
* Technician management
* Support ticket management
* Ticket priority:

  * Low
  * Medium
  * High
  * Critical
* Ticket status:

  * Open
  * In Progress
  * Resolved
  * Closed
* Assigning technicians to support tickets
* Automatic ticket transition from `OPEN` to `IN_PROGRESS` when a technician is assigned
* Preventing technician assignment to tickets that are no longer `OPEN`

## Current Architecture

The project is being developed in stages.

Current application structure:

```text
CLI
 ↓
Services
 ↓
Models
```

Repositories, database persistence, API development, Docker, and CI/CD will be introduced in later stages.

## Project Structure

```text
it_asset_management/
├── app/
│   ├── __init__.py
│   ├── exceptions/
│   │   └── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── asset.py
│   │   ├── employee.py
│   │   ├── laptop.py
│   │   ├── monitor.py
│   │   ├── phone.py
│   │   ├── technician.py
│   │   └── ticket.py
│   ├── repositories/
│   │   └── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── asset_service.py
│   │   ├── assignment_service.py
│   │   ├── employee_service.py
│   │   ├── technician_service.py
│   │   └── ticket_service.py
│   └── utils/
│       ├── __init__.py
│       └── enums.py
├── main.py
├── README.md
├── requirements.txt
└── tests/
```

## Implemented OOP Concepts

The current implementation demonstrates:

* Classes and objects
* Constructors
* Instance attributes
* Instance methods
* Inheritance
* Method overriding
* `super()`
* Composition
* Python dictionaries for in-memory storage
* Python lists for object relationships
* Enumerations using `Enum`
* Basic business rules

## Development Roadmap

The project will be developed through the following stages:

1. Python OOP foundation
2. Business logic / service layer
3. Repository layer
4. Custom exceptions
5. CLI
6. Testing
7. PostgreSQL database integration
8. FastAPI
9. Docker
10. CI/CD
11. Deployment, monitoring, and logging

## Current Status

The OOP models and initial business-logic services have been implemented.

The current system uses **in-memory storage**, so data is reset whenever the application stops. Persistent storage will be introduced during the database stage.

## Git Workflow

The project uses Git throughout development.

Feature branches are used for individual development stages, and completed milestones are committed and pushed before being merged into `main`.

Release tags will be introduced during the Docker/release stage.
