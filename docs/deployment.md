# Deployment

## Deployment target

The project is compatible with deployment platforms such as Render. The repository includes a [render.yaml](../render.yaml) configuration file.

## Runtime considerations

For deployment, ensure the following are configured:

- database environment variables
- `PYTHON_KEY` if protected routes are used
- `GEMINI_API_KEY` for prompt generation
- `RESEND_API_KEY` for email sending
- `BASE_URL` for environment-aware metadata

## Recommended deployment checklist

1. Set all required environment variables
2. Ensure PostgreSQL is available and reachable
3. Install Python dependencies
4. Run the application with Uvicorn or the deployment platform's startup command
5. Verify core endpoints such as `/health` and `/docs`

## Notes

Because the app depends on external services and a database, deployment should be treated as a full-stack environment rather than a simple static app.
