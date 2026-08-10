# Architecture

## Runtime stack

The application is built around the following core components:

- FastAPI for HTTP routing and request handling
- PostgreSQL for persistent storage
- Pydantic for request/response validation
- Uvicorn as the ASGI server
- Python dotenv for environment configuration

## Application entry point

The main application is initialized in [app/main.py](../app/main.py). It creates the FastAPI app, configures CORS, mounts static files, and includes the API router.

## Router structure

The main router is assembled in [app/api/routes.py](../app/api/routes.py). It includes multiple route modules for:

- root metadata
- health checks
- prompt endpoints
- prospects
- orders
- queue routes
- notifications
- GitHub, Flickr, and YouTube integrations

## Request flow

A typical request follows this pattern:

1. The FastAPI app receives an HTTP request
2. A route handler validates or parses input
3. The handler connects to PostgreSQL through the database utilities
4. Queries or updates are executed
5. A standardized response payload is returned using the shared metadata helper

## Core modules

### app/main.py

Defines the application object and global middleware.

### app/api

Contains the route modules and feature-specific endpoints.

### app/utils

Contains shared support code for:

- database connections
- API-key authentication
- response metadata
- health checks

## Design characteristics

The architecture favors a simple, service-oriented approach:

- route modules are feature focused
- database access is centralized
- shared metadata responses keep output consistent
- integrations are isolated into dedicated modules
