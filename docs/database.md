# Database

## Storage approach

The application relies on PostgreSQL for persistent storage. Database connection helpers are defined in [app/utils/db.py](../app/utils/db.py).

## Main data areas

The app uses several logical data areas:

- prospects
- prompt history
- orders
- queue-related records
- platform-specific tables for GitHub, Flickr, and YouTube

## Search capabilities

The README describes PostgreSQL full-text search support for prospects using `tsvector` and a GIN index. This allows efficient search across text fields.

## Why the database is central

The database is the system of record for most application features. It provides:

- reliable persistence
- filtering and pagination support
- search ability
- historical storage for AI prompt outputs and business records

## Operational note

The app expects database connection settings to be present in the environment. If the database is unavailable, many endpoints will not function properly.
