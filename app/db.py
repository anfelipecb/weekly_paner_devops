"""Database connection and helpers for PostgreSQL."""
import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    """Return a DB connection. Uses DATABASE_URL or individual env vars."""
    url = os.environ.get("DATABASE_URL")
    if url:
        return psycopg2.connect(url, cursor_factory=RealDictCursor)
    return psycopg2.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ.get("PGPORT", "5432"),
        dbname=os.environ.get("PGDATABASE", "planner"),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD", ""),
        cursor_factory=RealDictCursor,
    )


def fetch_tasks(day_of_week=None):
    """Fetch tasks, optionally filtered by day (1=Mon, 5=Fri)."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            if day_of_week is not None:
                cur.execute(
                    "SELECT id, day_of_week, title, completed, created_at FROM tasks WHERE day_of_week = %s ORDER BY id",
                    (day_of_week,),
                )
            else:
                cur.execute(
                    "SELECT id, day_of_week, title, completed, created_at FROM tasks ORDER BY day_of_week, id"
                )
            rows = cur.fetchall()
    return [dict(r) for r in rows]


def create_task(day_of_week, title):
    """Insert a task and return it."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (day_of_week, title) VALUES (%s, %s) RETURNING id, day_of_week, title, completed, created_at",
                (day_of_week, title),
            )
            row = cur.fetchone()
        conn.commit()
    return dict(row)


def update_task_completed(task_id, completed):
    """Set completed flag for a task. Returns updated task or None."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET completed = %s WHERE id = %s RETURNING id, day_of_week, title, completed, created_at",
                (completed, task_id),
            )
            row = cur.fetchone()
        conn.commit()
    return dict(row) if row else None
