"""Weekly planner Flask application."""
import os
from flask import Flask

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"),
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
)

from app import routes  # noqa: E402, F401
