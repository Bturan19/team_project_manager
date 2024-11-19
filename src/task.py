# src/task.py
import pandas as pd
from src.db import get_connection

def create_task(title, description, status, tags, project_id, sprint_id=None):  
    conn = get_connection()  
    c = conn.cursor()  
    try:  
        c.execute('''  
            INSERT INTO tasks (title, description, status, tags, project_id, sprint_id)  
            VALUES (?, ?, ?, ?, ?, ?)  
        ''', (title, description, status, tags, project_id, sprint_id))  
        conn.commit()  
    except Exception as e:  
        print(f"Error inserting task: {e}")  
    finally:  
        conn.close() 

def get_all_tasks():
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT tasks.*, projects.name AS project_name, projects.color AS project_color, sprints.name AS sprint_name  
        FROM tasks  
        LEFT JOIN projects ON tasks.project_id = projects.id  
        LEFT JOIN sprints ON tasks.sprint_id = sprints.id 
    ''', conn)
    conn.close()
    return df


def update_task(task_id, title, description, status, tags, project_id, sprint_id=None):  
    conn = get_connection()  
    c = conn.cursor()  
    try:  
        c.execute('''  
            UPDATE tasks  
            SET title = ?, description = ?, status = ?, tags = ?, project_id = ?, sprint_id = ?  
            WHERE id = ?  
        ''', (title, description, status, tags, project_id, sprint_id, task_id))  
        conn.commit()  
    except Exception as e:  
        print(f"Error updating task: {e}")  
    finally:  
        conn.close() 

def delete_task(task_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()