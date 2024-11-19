# src/sprint.py
import pandas as pd
from src.db import get_connection

def create_sprint(name, start_date, end_date):  
    conn = get_connection()  
    c = conn.cursor()  
    c.execute('''  
        INSERT INTO sprints (name, start_date, end_date)  
        VALUES (?, ?, ?)  
    ''', (name, start_date, end_date))  
    conn.commit()  
    conn.close() 

def update_sprint(sprint_id, name, start_date, end_date, is_active):  
    conn = get_connection()  
    c = conn.cursor()  
    try:  
        c.execute('''  
            UPDATE sprints  
            SET name = ?, start_date = ?, end_date = ?, is_active = ?  
            WHERE id = ?  
        ''', (name, start_date, end_date, is_active, sprint_id))  
        conn.commit()  
    except Exception as e:  
        print(f"Error updating sprint: {e}")  
    finally:  
        conn.close() 

def get_all_sprints(active_only=False):  
    conn = get_connection()  
    query = 'SELECT * FROM sprints'  
    if active_only:  
        query += ' WHERE is_active = 1'  
    df = pd.read_sql_query(query, conn)  
    conn.close()  
    return df  

def close_sprint(sprint_id):  
    conn = get_connection()  
    c = conn.cursor()  
    c.execute('''  
        UPDATE sprints  
        SET is_active = 0  
        WHERE id = ?  
    ''', (sprint_id,))  
    conn.commit()  
    conn.close()  

def get_sprint_tasks(sprint_id):  
    conn = get_connection()  
    df = pd.read_sql_query('SELECT * FROM tasks WHERE sprint_id = ?', conn, params=(sprint_id,))  
    conn.close()  
    return df  