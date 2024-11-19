# src/db.py
import os
import sqlite3
from pathlib import Path

# Define the path to the database file
DB_PATH = Path(__file__).parent.parent / "data" / "task_manager.db"
DB_PATH = "/tmp/task_manager.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn