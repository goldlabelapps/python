# API Reference

## Core endpoints

### Root

- `GET /` — returns basic service metadata such as title, version, and base URL

### Health

- `GET /health` — health check endpoint used to confirm the service is available

### Prompt endpoints

- `GET /prompt` or `GET /prompts` — returns metadata for the prompt table, including row count and columns
- `POST /prompt` — accepts a prompt payload and returns either cached output or a generated response from Gemini

### Prospects

- `GET /prospects` — returns paginated prospects, with optional filtering and search
- `GET /prospects/{id}` — returns one prospect and any related prompt records
- `PATCH /prospects/{id}` — updates flag and hide state
- `PATCH /prospects/factoryreset` — resets prospect flags and hidden state

### Orders

- `GET /orders` — returns paginated and filterable order data

### Queue routes

The queue module exposes routes for creating, reading, deleting, emptying, and altering queue-related data.

### Notifications

- `GET /notify/email` — returns usage information for the email endpoint
- `POST /notify/email` — sends an email through Resend

### External data endpoints

- `GET /github` — returns GitHub-related table data
- `GET /flickr` — returns Flickr-related table data
- `GET /youtube` — returns YouTube-related table data

## Response style

Most endpoints return a response object shaped like:

```json
{
  "meta": {
    "status": "success",
    "message": "..."
  },
  "data": {}
}
```

## Authentication

Some routes depend on an API key header:

```http
X-API-Key: your_key
```

The key is validated through the shared authentication utility.
