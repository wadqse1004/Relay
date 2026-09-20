# Database Design

DBMS: PostgreSQL

## Naming Rules

- Table: snake_case
- Column: snake_case
- PK: id
- FK: {entity}\_id
- Boolean: is_xxx
- Created: created_by, created_at
- Updated: updated_by, updated_at

## PK Rule

Use:

BIGINT GENERATED ALWAYS AS IDENTITY

## Common Code

- code_groups
- common_codes

## Core Domains

- Organization / Master
- Approval / Leave
- Issue Tracking
- Collaboration
- Notification
- Audit
