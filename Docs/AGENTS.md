# Relay Agent Rules

## Project Goal

Build an internal company workflow platform.

Core features:

- leave / half-day request and approval
- internal issue tracking
- employee and department management
- internal collaboration
- notifications

## Tech Stack

Frontend:

- React
- TypeScript
- Vite

Backend:

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic

Database:

- PostgreSQL

## Repository Structure

/frontend
/backend
/database
/docs

## Development Rules

- Work incrementally.
- Do not implement future-stage features unless explicitly requested.
- Do not modify unrelated files.
- Avoid unnecessary abstraction.
- Reuse existing structure and conventions.
- Inspect existing code before making changes.
- Run available tests/build/type checks after changes.

## Database Rules

- Use snake_case.
- Use BIGINT GENERATED ALWAYS AS IDENTITY for PK.
- Use BOOLEAN for true/false values.
- Use code_groups/common_codes for simple master codes.
- Use separate master tables for entities with relationships.
- Business/master tables should include:
  - created_by
  - created_at
  - updated_by
  - updated_at

## Architecture

Backend:

Router
→ Service
→ Repository
→ Database

Frontend:

pages
components
hooks
api
types

## MVP Scope

Do not introduce these unless explicitly requested:

- Redis
- Kafka
- Docker
- Kubernetes
- WebSocket
