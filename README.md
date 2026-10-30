# CareerOS

**A Python backend API for managing job applications and organizing the job search.**

CareerOS is a REST API that helps users track job applications, manage application details, and organize their job search.

The project is built using Python, FastAPI, and PostgreSQL, with an emphasis on backend engineering fundamentals, database integrity, API validation, authentication foundations, and automated testing.

**Tech Stack:** Python · FastAPI · PostgreSQL · SQLAlchemy · Pydantic · Alembic · pytest

[GitHub Repository](https://github.com/purna9101/CareerOS)

## Current Features

### Application Management

- Create, retrieve, update, and delete job applications.
- Retrieve applications using company, position, and status filters.
- Validate incoming application data.
- Normalize application status values.

### User Registration

- Register users with a username, email, and password.
- Validate email addresses and password requirements using Pydantic.
- Prevent duplicate usernames and email addresses.
- Hash passwords using Argon2 through `pwdlib`.
- Store user credentials securely using a hashed-password field.
- Return a dedicated response schema that excludes passwords and password hashes.

### Database and Reliability

- PostgreSQL persistence using SQLAlchemy ORM.
- Database-level constraints for data integrity.
- Version-controlled database migrations using Alembic.
- Global exception handling that avoids exposing internal error details.
- Automated API testing using pytest and a dedicated PostgreSQL test database.

## Architecture

CareerOS follows a layered backend architecture that separates request validation, API logic, database access, and persistence.

### Application request flow

```mermaid
flowchart TD
    A["Client Request"] --> B["FastAPI Router"]
    B --> C{"Pydantic Validation"}

    C -->|Invalid| D["HTTP 422 Response"]
    C -->|Valid| E["API Endpoint"]

    E --> F["Database Dependency"]
    F --> G["SQLAlchemy Session"]
    G <--> H[("PostgreSQL")]

    E -->|Record Not Found| I["HTTP 404 Response"]
    E -->|Unexpected Error| J["Exception Handler"]
    J --> K["HTTP 500 Response"]

    G --> L["Response Serialization"]
    L --> M["HTTP Response"]
```

### User registration flow

```mermaid
flowchart TD
    A["Registration Request"] --> B["UserCreate Schema"]
    B --> C{"Input Valid?"}

    C -->|No| D["HTTP 422 Response"]
    C -->|Yes| E["Check Existing Username / Email"]

    E -->|Already Exists| F["HTTP 409 Conflict"]
    E -->|Available| G["Hash Password"]

    G --> H["Create User ORM Object"]
    H --> I["SQLAlchemy Session"]
    I --> J[("PostgreSQL")]

    J --> K["UserResponse Schema"]
    K --> L["Return User Details"]
```

### Component responsibilities

| Component  | Responsibility                                                    |
| ---------- | ----------------------------------------------------------------- |
| FastAPI    | HTTP routing, endpoint execution, and dependency injection        |
| Pydantic   | Request validation, field constraints, and response serialization |
| SQLAlchemy | ORM models, database sessions, and database operations            |
| PostgreSQL | Persistent storage and database-level integrity                   |
| Alembic    | Version-controlled database schema changes                        |
| pwdlib     | Password hashing and verification                                 |
| pytest     | Automated API and application testing                             |

## Database Design and Integrity

CareerOS uses PostgreSQL for persistent storage and SQLAlchemy ORM for database interaction.

### Applications table

Stores job application records.

| Column     | Purpose                                                      |
| ---------- | ------------------------------------------------------------ |
| `id`       | Primary key                                                  |
| `company`  | Required company name; indexed                               |
| `position` | Required job position                                        |
| `status`   | Required application status with a database check constraint |

Supported application statuses:

`applied`, `interview`, `offer`, `selected`, `rejected`, `ghosted`

### Users table

Stores registered user information.

| Column            | Purpose                                           |
| ----------------- | ------------------------------------------------- |
| `id`              | Primary key                                       |
| `username`        | Required and unique username                      |
| `email`           | Required and unique email address                 |
| `hashed_password` | Password hash; never stores the original password |

### Data integrity

- NOT NULL constraints prevent missing required values.
- Unique constraints prevent duplicate usernames and email addresses.
- A status check constraint restricts application statuses to supported values.
- Alembic migrations make database schema changes explicit and reviewable.

## Validation and Error Handling

CareerOS validates incoming data before processing database operations.

### Request validation

- Required text fields reject empty or whitespace-only values.
- Company and position fields enforce maximum lengths.
- Application statuses are restricted to supported values.
- User email addresses are validated using `EmailStr`.
- Registration passwords require at least eight characters.

### HTTP error handling

| Status | Meaning                         |
| ------ | ------------------------------- |
| `200`  | Successful request              |
| `404`  | Requested application not found |
| `409`  | Duplicate username or email     |
| `422`  | Request validation failed       |
| `500`  | Unexpected server error         |

Unexpected errors are logged internally without exposing exception details to API clients.

## Password Security

User registration uses password hashing rather than storing plaintext passwords.

The implementation uses `pwdlib` with its recommended Argon2 configuration.

Password handling flow:

1. Receive the password through the registration request.
2. Hash the password using `hash_password()`.
3. Store the resulting hash in `hashed_password`.
4. Exclude password-related fields from API responses.

The API uses separate Pydantic schemas for incoming user data (`UserCreate`) and outgoing user data (`UserResponse`).

## Testing

CareerOS uses pytest and FastAPI's test client.

The existing application test suite covers CRUD operations, request validation, and error handling.

Tests use a dedicated PostgreSQL test database separate from the application database. FastAPI dependency overrides allow database access to be controlled during testing.

Registration has also been manually verified through Swagger UI for:

- Successful user registration.
- Duplicate username or email rejection.
- Password minimum-length validation.
- Safe response serialization.

Run automated tests:

```bash
pytest -v
```

## API Reference

Interactive API documentation is available through FastAPI Swagger UI at `/docs`.

### Application endpoints

| Method   | Endpoint                         | Description                             |
| -------- | -------------------------------- | --------------------------------------- |
| `POST`   | `/applications`                  | Create an application                   |
| `GET`    | `/applications`                  | List applications with optional filters |
| `GET`    | `/applications/{application_id}` | Retrieve an application                 |
| `PUT`    | `/applications/{application_id}` | Replace an application                  |
| `PATCH`  | `/applications/{application_id}` | Partially update an application         |
| `DELETE` | `/applications/{application_id}` | Delete an application                   |

### User endpoints

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| `POST` | `/users/register` | Register a new user |

### Registration example

**Request:**

`POST /users/register`

```json
{
  "username": "arjun",
  "email": "arjun@example.com",
  "password": "secret123"
}
```

**Successful response:**

```json
{
  "id": 1,
  "username": "arjun",
  "email": "arjun@example.com"
}
```

## Getting Started

### Prerequisites

- Python
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/purna9101/CareerOS.git
cd CareerOS
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it using Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Configure your PostgreSQL connection:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/careeros
```

Replace the placeholder with your local PostgreSQL credentials.

Never commit `.env` files or database credentials.

### 5. Apply database migrations

```bash
alembic upgrade head
```

### 6. Start the development server

```bash
uvicorn app.main:app --reload
```

Open the following URL to access Swagger UI:

`http://127.0.0.1:8000/docs`

## Engineering Focus

CareerOS is being developed incrementally using a practical backend engineering workflow:

**Understand → Reason → Implement → Test → Review → Commit → Explain**

The project focuses on:

- REST API design and HTTP semantics.
- Relational database design and integrity.
- Secure password handling.
- Request validation and error handling.
- Database migrations.
- Automated testing and maintainable code.

## Future Development

Planned improvements include:

- User login and JWT-based authentication.
- Protected endpoints and per-user application ownership.
- Resume upload and association with job applications.
- Application analytics and job-search insights.
- Docker-based deployment and CI/CD automation.

---

**CareerOS — Building a practical foundation in Python backend engineering.**
