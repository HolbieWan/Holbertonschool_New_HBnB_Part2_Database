#!/usr/bin/env python3
"""
Entry point for the application.
This script initializes the Flask app, sets up the database,
and runs the server.
"""

from app import create_app
from app.extensions import db

app = create_app('development')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
