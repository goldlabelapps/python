# Project Documentation

This directory contains the main documentation for the Python backend service in this repository.

## Documentation map

- [Overview](overview.md) — What the application does and why it exists
- [Architecture](architecture.md) — Application structure, runtime flow, and major components
- [Setup](setup.md) — Installation, environment variables, and local development
- [API Reference](api.md) — Routes, request patterns, and response shape
- [Integrations](integrations.md) — Gemini, email, and third-party data connectors
- [Database](database.md) — PostgreSQL usage, schemas, and search capabilities
- [Testing](testing.md) — How the project is tested and how to run tests
- [Deployment](deployment.md) — Render-style deployment considerations and runtime configuration

## Quick start

1. Install dependencies with `pip install -r requirements.txt`
2. Create a local environment file with the required variables
3. Start the app with `uvicorn app.main:app --reload`
4. Open the interactive documentation at `/docs`

## Project summary

This repository is a FastAPI-based backend that exposes APIs for data storage, retrieval, and automation. It is designed to support business workflows involving prospects, prompts, orders, queue operations, and integrations with external services.
