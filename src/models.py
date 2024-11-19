# src/models.py  
import sqlite3  
from src.db import get_connection  
  
def initialize_database():  
    conn = get_connection()  
    c = conn.cursor()  
  
    # Update the projects table to include start_date and estimated_end_date  
    c.execute('''  
    CREATE TABLE IF NOT EXISTS projects (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        name TEXT NOT NULL UNIQUE,  
        description TEXT,  
        start_date DATE,  
        estimated_end_date DATE,  
        color TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
    )  
    ''')  
  
    # Remove project_id from sprints table  
    c.execute('''  
    CREATE TABLE IF NOT EXISTS sprints (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        name TEXT NOT NULL,  
        start_date DATE,  
        end_date DATE,  
        is_active INTEGER DEFAULT 1,  
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
    )  
    ''')  
  
    c.execute('''  
    CREATE TABLE IF NOT EXISTS tasks (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        title TEXT NOT NULL,  
        description TEXT,  
        status TEXT NOT NULL,  
        tags TEXT,  
        project_id INTEGER,  
        sprint_id INTEGER,  
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
        FOREIGN KEY (project_id) REFERENCES projects (id),  
        FOREIGN KEY (sprint_id) REFERENCES sprints (id)  
    )  
    ''')  
  
    c.execute('''  
    CREATE TABLE IF NOT EXISTS knowledge_base (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        title TEXT NOT NULL,  
        content TEXT NOT NULL,  
        tags TEXT,  
        project_id INTEGER,  
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
        FOREIGN KEY (project_id) REFERENCES projects (id)  
    )  
    ''')  
    conn.commit()  
    conn.close()  