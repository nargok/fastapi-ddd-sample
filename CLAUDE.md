# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based DDD (Domain-Driven Design) sample application implementing an attendance management system. The project uses a 4-layer architecture: Presentation, Application, Domain, and Infrastructure.

## Development Commands

### Setup & Dependencies
```bash
# Install dependencies using uv (Python 3.13+)
uv sync

# Activate virtual environment
source .venv/bin/activate
```

### Running the Application
```bash
# Start the FastAPI development server
uvicorn app.main:app --reload
```

### Type Checking & Linting
```bash
# Run type checking with MyPy
uv run mypy app/

# Run tests with pytest
uv run pytest
```

## Architecture

The application follows Domain-Driven Design with these layers:

### Layer Structure
```
app/
├── presentation/     # API routes, schemas (Pydantic DTOs), error handlers
├── application/      # Use cases, DTOs, orchestration services
├── domain/          # Core business logic
│   ├── models/      # Entities, aggregates, value objects
│   ├── repositories/ # Repository abstractions (ports)
│   ├── services/    # Domain services, business rules
│   └── events/      # Domain events
└── infrastructure/  # Implementations
    ├── repositories/ # InMemory repository implementations
    └── messaging/   # Event publisher implementations
```

### Dependency Direction
- Presentation → Application → Domain
- Infrastructure implements Domain ports
- Domain layer has no dependencies on other layers

## Domain Model

Key aggregates and entities as specified in docs/spec.md:

- **Timesheet** (Aggregate Root): Monthly attendance record containing daily AttendanceEntry items
- **AttendanceEntry**: Daily attendance with state transitions (ClockedOut → ClockedIn → OnBreak → ClockedIn → ClockedOut)
- **OvertimeRequest**: Overtime request aggregate
- **LeaveRequest**: Leave request aggregate

## Implementation Guidelines

### State Management
- All data is stored in-memory only (no database persistence)
- Repository implementations use dictionaries for storage
- Data is lost on server restart

### API Design
- MVP endpoints (v1): Clock-in/out, break management, daily/monthly views
- Extended endpoints (v2): Timesheet submission/approval, overtime/leave requests
- Authentication via `X-EMPLOYEE-ID` header (simplified for demo)

### Error Handling
- 400: Invalid input or state transition violations
- 404: Resource not found
- 409: Conflicts (e.g., editing submitted timesheets)
- 422: Schema validation errors

### Testing Strategy
- Domain unit tests: Focus on invariants, state transitions, calculations
- Application tests: Use case scenarios
- API tests: Using FastAPI TestClient

## Current Implementation Status

The project structure is initialized with:
- Basic FastAPI setup with a `/ping` endpoint
- Empty directory structure following DDD layers
- Detailed specification in `docs/spec.md`

Next implementation steps should follow the task breakdown in the specification:
1. Create domain value objects and entities
2. Define repository abstractions
3. Implement in-memory repositories
4. Create use cases starting with clock_in, start_break, end_break, clock_out
5. Implement v1 API endpoints
6. Add monthly summary calculation
7. Write tests for each layer
8. Extend with v2 features (requests and approvals)