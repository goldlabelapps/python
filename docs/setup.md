# Setup and Local Development

## Requirements

- Python 3.11 or newer
- PostgreSQL access
- Optional: environment variables for AI and email services

## Installation

From the repository root:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

Create a local environment file and configure the required values:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
BASE_URL=http://localhost:8000
PYTHON_KEY=your_api_key
GEMINI_API_KEY=your_gemini_key
RESEND_API_KEY=your_resend_key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

> Important: if the API is called from a browser frontend, the frontend origin must be explicitly listed in `ALLOWED_ORIGINS`. This is a common deployment gotcha. If your app is hosted at a production URL such as `https://your-app.example.com`, add that exact origin to the environment variable before deploying.

## Running the app

Start the development server:

```bash
uvicorn app.main:app --reload
```

The service will then be available at:

- http://localhost:8000
- http://localhost:8000/docs for Swagger UI

## Static assets

Static files are mounted under `/static` from the application’s static folder.

## Notes

- Some endpoints require the API key header `X-API-Key`
- If the database is not configured correctly, many endpoints will fail at runtime
- The app expects the database schema to exist before it can serve data reliably
