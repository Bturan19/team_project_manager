# src/project.py
import pandas as pd
from src.db import get_connection

def create_project(name, description, start_date, estimated_end_date, color):  
    conn = get_connection()  
    c = conn.cursor()  
    c.execute('''  
        INSERT INTO projects (name, description, start_date, estimated_end_date, color)  
        VALUES (?, ?, ?, ?, ?)  
    ''', (name, description, start_date, estimated_end_date, color))  
    conn.commit()  
    conn.close()  

def update_project(project_id, name, description, start_date, estimated_end_date, color):  
    conn = get_connection()  
    c = conn.cursor()  
    try:  
        c.execute('''  
        UPDATE projects  
        SET name = ?, description = ?, start_date = ?, estimated_end_date = ?, color = ?  
        WHERE id = ?  
    ''', (name, description, start_date, estimated_end_date, color, project_id)) 
        conn.commit()  
    except Exception as e:  
        print(f"Error updating project: {e}")  
    finally:  
        conn.close() 

def get_all_projects():
    conn = get_connection()
    df = pd.read_sql_query('SELECT * FROM projects', conn)
    conn.close()
    return df

def get_project_by_id(project_id):
    conn = get_connection()
    df = pd.read_sql_query(
        'SELECT * FROM projects WHERE id = ?', conn, params=(project_id,))
    conn.close()
    return df