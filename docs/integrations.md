# Integrations

## Gemini / Google AI

The prompt endpoint uses the Google GenAI client to generate completions when no suitable cached response is found.

Key points:

- the application reads `GEMINI_API_KEY` from the environment
- prompt requests can be cached in the database
- generated responses are stored with metadata such as model and prompt hash

## Resend email

The notify module sends email messages through Resend.

Key points:

- the application reads `RESEND_API_KEY` from the environment
- the endpoint accepts recipient, subject, and HTML content
- a template wrapper is used for consistent outbound email formatting

## GitHub, Flickr, and YouTube

Separate route modules expose endpoints that read from database tables associated with those platforms.

These integrations are designed to provide a simple API layer over data that has already been imported or synced into the system.

## General design

The integration modules are intentionally isolated so that:

- external services can be replaced or extended easily
- database access remains centralized
- route code stays simple and focused on HTTP behavior
