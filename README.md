## I

> FastAPI/Python/Postgres/tsvector. 
Open Source, production ready Python FastAPI/Postgres app for [NX](https://goldlabel.pro?s=python-nx-ai)

```sh
uvicorn app.main:app  --reload
```

#### Install

Create an environment file and add Postgres credentials etc

`cp .env.sample .env`

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is at <http://localhost:8000>.

[localhost](http://localhost:8000) | [Public RESTful API](https://nx-ai.onrender.com) 

- **Python 3.11+**
- **Postgres**
- **tsvector** - Superfast full-text search (with GIN index)
### Full-Text Search (tsvector)

The prospects table includes a `search_vector` column (type: tsvector) that is automatically computed from all text fields on insert. A GIN index is created for this column, enabling fast and scalable full-text search queries.

**How it works:**
- On every insert (via `/prospects/seed` or `/prospects/process`), the `search_vector` is computed from all text columns using PostgreSQL's `to_tsvector('english', ...)`.
- The GIN index (`idx_prospects_search_vector`) allows efficient search queries like:

```sql
SELECT * FROM prospects WHERE search_vector @@ plainto_tsquery('english', 'search terms');
```

This makes searching across all text fields in the prospects table extremely fast, even for large datasets.
- **FastAPI** — RESTful API framework
- **Uvicorn** — ASGI server
- **Pytest** — testing framework
- **HTTPX / TestClient**

FastAPI automatically generates interactive documentation:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

#### Structure

```
app/
  __init__.py
  main.py          # FastAPI application entry point
  api/
    __init__.py
    routes.py      # API endpoint definitions
tests/
  __init__.py
  test_routes.py   # Unit and integration tests
requirements.txt
```


#### Endpoints

| Method | Path      | Description                     |
|--------|-----------|---------------------------------|
| GET    | `/`       | Welcome message                 |
| GET    | `/health` | Health check — returns `ok`     |
| POST   | `/echo`   | Echoes the JSON `message` field |
| GET    | `/prospects/seed` | (Re)create prospects table and seed with sample data |
| DELETE | `/prospects/process` | (Legacy) Empties the prospects table |
| GET    | `/prospects/process` | Process and insert all records from big.csv into prospects table |

### Processing Large CSV Files

The `/prospects/process` endpoint is designed for robust, scalable ingestion of large CSV files (e.g., 1300+ rows, 300KB+). It follows the same normalization and insertion pattern as `/prospects/seed`, but is optimized for large files:


#### Example usage

1. Seed the table structure:
  - `GET /prospects/seed`
2. (Optional) Empty the table:
  - `DELETE /prospects/empty`
3. Process the large CSV:
  - `GET /prospects/process`

The endpoint will return the number of records inserted. This is the core ingestion workflow for production-scale data.


