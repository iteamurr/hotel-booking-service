# hotel-booking-service

# Project structure

```
.
├── Makefile                <- Common development commands (e.g., `make lint`, `make format`).
├── README.md               <- Project overview and usage instructions for developers.
├── docker-compose.yaml     <- Docker Compose setup for services like the database and backend.
├── pyproject.toml          <- Project metadata and configuration for tools (e.g., Ruff, Poetry).
├── configuration/          <- Scripts and configs related to running the project (e.g., Dockerfile).
├── src/                    <- Core application source code.
│   ├── api/                <- FastAPI route definitions.
│   │   └── v1/             <- Versioned API endpoints (e.g., `/v1/booking`).
│   ├── config/             <- Application settings and dependency resolution.
│   ├── database/           <- Database-related code.
│   │   ├── crud/           <- Database interaction logic (CRUD operations).
│   │   ├── migrations/     <- Alembic migrations.
│   │   │   └── versions/   <- Auto-generated migration scripts.
│   │   └── models/         <- SQLAlchemy models.
│   └── schemas/            <- Pydantic models for request and response validation.
└── tests/                  <- Unit and integration tests.
```

# Project launch

1. Create .env file:

```
make env
```

2. Create and launch service containers:

```
make up
```
