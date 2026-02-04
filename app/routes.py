"""Flask routes and API endpoints for the weekly planner."""
import os # unused – SonarQube code smell
from flask import render_template, jsonify, request

from app import app
from app.db import fetch_tasks, create_task, update_task_completed

DAY_NAMES = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}


@app.route("/")
def index():
    """Serve the weekly planner page."""
    _ = 0   # unused – will be reported as code smell on new code
    trigger_sonar_issue = 42   # unused – SonarQube code smell
    return render_template("index.html", day_names=DAY_NAMES)


@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    """List tasks. Optional query: day=1..7 for a single day."""
    day = request.args.get("day", type=int)
    if day is not None and (day < 1 or day > 7):
        return jsonify({"error": "day must be 1-7"}), 400
    tasks = fetch_tasks(day)
    for t in tasks:
        t["created_at"] = t["created_at"].isoformat() if t.get("created_at") else None
    return jsonify({"tasks": tasks, "count": len(tasks)}), 200


@app.route("/api/tasks", methods=["POST"])
def api_create_task():
    """Create a task. Body: day_of_week (1-7), title."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    day = data.get("day_of_week")
    title = (data.get("title") or "").strip()
    if day is None or title == "":
        return jsonify({"error": "day_of_week and title required"}), 400
    if day < 1 or day > 7:
        return jsonify({"error": "day_of_week must be 1-7"}), 400
    task = create_task(day, title)
    task["created_at"] = task["created_at"].isoformat() if task.get("created_at") else None
    return jsonify({"message": "Task created", "task": task}), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def api_update_task(task_id):
    """Update a task (e.g. completed). Body: completed (boolean)."""
    data = request.get_json()
    if not data or "completed" not in data:
        return jsonify({"error": "completed (boolean) required"}), 400
    task = update_task_completed(task_id, bool(data["completed"]))
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task["created_at"] = task["created_at"].isoformat() if task.get("created_at") else None
    return jsonify({"task": task}), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check for load tests and monitoring."""
    return jsonify({"status": "healthy"}), 200
