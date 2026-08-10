# Testing

## Test framework

The project uses `pytest` for automated tests.

## Running tests

From the repository root:

```bash
pytest
```

## Existing test areas

The repository includes tests for:

- GitHub integration behavior
- health endpoints
- metadata helpers
- orders
- prompts
- prospects
- queue routes
- resend email behavior
- route registration

## Testing approach

The tests appear to validate behavior at the route and utility level, focusing on expected API responses and core functionality rather than UI interaction.
