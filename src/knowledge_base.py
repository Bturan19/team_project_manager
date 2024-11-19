# src/knowledge_base.py
import pandas as pd
from src.db import get_connection

def add_knowledge_entry(title, content, tags, project_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO knowledge_base (title, content, tags, project_id)
        VALUES (?, ?, ?, ?)
    ''', (title, content, tags, project_id))
    conn.commit()
    conn.close()

def get_all_knowledge_entries():
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT knowledge_base.*, projects.name AS project_name
        FROM knowledge_base
        LEFT JOIN projects ON knowledge_base.project_id = projects.id
    ''', conn)
    conn.close()
    return df