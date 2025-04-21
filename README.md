# hotel-booking-service

# Project structure

```
.
├── Makefile                <- Common development commands.
├── README.md               <- Project overview and usage instructions.
├── docker-compose.yaml     <- Docker Compose setup for services.
├── pyproject.toml          <- Project metadata and configuration for tools.
├── config/                 <- Scripts related to running the project.
├── src/                    <- Core application source code.
│   ├── application/        <- Business logic layer with features.
│   │   ├── booking/        <- Booking-related code.
│   │   │   └── interfaces  <- Interfaces for booking functionality.
│   │   └── hotel/          <- Hotel-related code.
│   │       └── interfaces  <- Interfaces for hotel functionality.
│   ├── domain/             <- Core domain logic (models and services).
│   │   ├── models/         <- Domain models representing key entities.
│   │   └── services/       <- Services containing business logic for the 
│   │                          application.
│   ├── infrastructure/     <- Infrastructure layer for external integrations
│   │                          and database interactions.
│   │   ├── config/         <- Application configuration files.
│   │   └── db/             <- Database-related components.
│   │       ├── migrations/ <- Database migrations (Alembic).
│   │       │   └── versions <- Auto-generated migration versions.
│   │       ├── models/     <- Database models.
│   │       └── repositories <- Repositories for interacting with the 
│   │                           database.
│   ├── presentation/       <- Presentation layer for API routes and schemas.
│   │   ├── api/            <- API route definitions.
│   │   │   └── routes/     <- API routes definitions (e.g., `/v1/booking`).
│   │   │       └── v1/     <- Version 1 of the API.
│   │   │           ├── booking/ <- Booking routes and dependencies.
│   │   │           ├── dependencies/ <- Common dependencies for the API.
│   │   │           └── hotel/ <- Hotel routes and dependencies.
│   │   └── schemas/        <- Pydantic models for request and response 
│   │                          validation.
│   └── shared_kernel/      <- Shared infrastructure components
│       │                      used across the app.
│       └── building_blocks/ <- Core reusable components for the application.
│           └── infrastructure/ <- Shared infrastructure utilities.
└── tests/                  <- Unit and integration tests.
    └── test_handlers/      <- Test cases for different application features.
        ├── booking/        <- Tests for booking functionality.
        └── hotel/          <- Tests for hotel functionality.
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
