# Weekly Planner (Mon–Sun)

This project contains a minimal Flask web application to track tasks by weekday (Monday through Sunday). The application uses a PostgreSQL backend, a Flask API, and a light, almost-white User Interface. The app is deployed with a CI/CD pipeline using Jenkins.

## Requirements

- [uv](https://docs.astral.sh/uv/) (Python package manager and runner)
- Python 3.9+ (uv will use it automatically)
- PostgreSQL (local or via `DATABASE_URL`)

## Database setup

The app connects to PostgreSQL using either a **connection URL** or **individual environment variables**. Use the same connection for (1) running the schema and seed scripts and (2) running the app.

### Connection options

| Variable        | Meaning              | Default (if unset) |
|----------------|----------------------|--------------------|
| `DATABASE_URL` | Full URL (overrides the rest) | — |
| `PGHOST`       | Database host        | `localhost`        |
| `PGPORT`       | Port                 | `5432`             |
| `PGDATABASE`   | Database name        | `planner`          |
| `PGUSER`       | Username             | `postgres`         |
| `PGPASSWORD`   | Password             | (empty)            |

Either set **`DATABASE_URL`** (e.g. `postgresql://user:password@host:5432/planner`) or set **`PGHOST`**, **`PGPORT`**, **`PGDATABASE`**, **`PGUSER`**, and **`PGPASSWORD`** as needed for your instance.

### Create the database and load schema + seed

**macOS with Homebrew:** PostgreSQL is often installed as `postgresql@15` or `postgresql@16`. The `createdb` and `psql` commands may not be on your PATH. Use the full path (replace `@15` with your version if different):

```bash
# Add PostgreSQL tools to PATH for this session (optional but convenient)
export PATH="$(brew --prefix postgresql@15)/bin:$PATH"

# On macOS/Homebrew the default DB user is usually your system username, not "postgres"
export PGUSER=$(whoami)
export PGDATABASE=planner

createdb planner
psql -d planner -f db/schema.sql
psql -d planner -f db/seed.sql
```

To make `createdb` and `psql` available in every terminal, add this line to `~/.zshrc`:

```bash
export PATH="$(brew --prefix postgresql@15)/bin:$PATH"
```

Then run the app with the same user: `export PGUSER=$(whoami) PGDATABASE=planner` before `uv run python app.py`.

**If you use local PostgreSQL with defaults** (host localhost, port 5432, user postgres, no password):

```bash
createdb planner
psql -d planner -f db/schema.sql
psql -d planner -f db/seed.sql
```

**If you use a custom host, user, or password**, set the same variables you will use for the app, then run the scripts. Example with env vars:

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=planner
export PGUSER=postgres
export PGPASSWORD=yourpassword

createdb planner   # or create the DB in your tool if remote
psql -d planner -f db/schema.sql
psql -d planner -f db/seed.sql
```

Example with a connection URL (run `psql` with that URL):

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/planner"
psql "$DATABASE_URL" -f db/schema.sql
psql "$DATABASE_URL" -f db/seed.sql
```

(If the database does not exist yet, create it first via your provider or `createdb`.)

## Run the app with uv

From the `planner_app` directory:

```bash
cd planner_app
uv sync
```

Set the same connection you used above (so the app can reach the database):

- **macOS (Homebrew):** set `PGUSER=$(whoami)` and `PGDATABASE=planner` (the app defaults to user `postgres`, which often doesn’t exist on Homebrew).
- **Local defaults (Linux, etc.):** often no env vars needed; if your DB has a password, set `PGPASSWORD`.
- **Custom/remote:** set `DATABASE_URL` or `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` before running.

```bash
# Example: local with password
export PGPASSWORD=yourpassword
uv run python app.py

# Example: custom host (same vars as in Database setup)
export PGHOST=myhost PGPORT=5432 PGDATABASE=planner PGUSER=myuser PGPASSWORD=mypass
uv run python app.py
```

Open http://localhost:5001 (default port is 5001 to avoid conflict with macOS AirPlay on 5000; set `PORT` to use another port)

Use `uv run` for any Python command (no need to activate a venv first):

```bash
uv run python app.py
uv run pytest
```

## API

- `GET /api/tasks` — list all tasks (optional `?day=1`..7 for one day)
- `POST /api/tasks` — create task (`{"day_of_week": 1-7, "title": "..."}`)
- `PATCH /api/tasks/<id>` — update task (`{"completed": true|false}`)
- `GET /health` — health check

Days: 1 = Monday … 7 = Sunday.

## Project layout

- `app/` — Flask app and DB helpers
- `db/schema.sql` — table creation for staging/production
- `db/seed.sql` — sample data for staging
- `templates/` — HTML
- `static/css/`, `static/js/` — minimal front end
- `pyproject.toml` — project config and dependencies (uv)
