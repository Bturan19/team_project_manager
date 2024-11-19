# src/sprint.py  
import pandas as pd  
from src.db import get_engine  
from sqlalchemy import text  
  
def create_sprint(name, start_date, end_date):  
    engine = get_engine()  
    with engine.begin() as conn:  
        conn.execute(  
            text('''  
                INSERT INTO sprints (name, start_date, end_date)  
                VALUES (:name, :start_date, :end_date)  
            '''),  
            {  
                'name': name,  
                'start_date': start_date,  
                'end_date': end_date  
            }  
        )  
  
def update_sprint(sprint_id, name, start_date, end_date, is_active):  
    engine = get_engine()  
    with engine.begin() as conn:  
        try:  
            conn.execute(  
                text('''  
                    UPDATE sprints  
                    SET name = :name, start_date = :start_date, end_date = :end_date, is_active = :is_active  
                    WHERE id = :sprint_id  
                '''),  
                {  
                    'name': name,  
                    'start_date': start_date,  
                    'end_date': end_date,  
                    'is_active': is_active,  
                    'sprint_id': sprint_id  
                }  
            )  
        except Exception as e:  
            print(f"Error updating sprint: {e}")  
  
def get_all_sprints(active_only=False):  
    engine = get_engine()  
    if active_only:  
        query = text('SELECT * FROM sprints WHERE is_active = TRUE')  
    else:  
        query = text('SELECT * FROM sprints')  
    df = pd.read_sql_query(query, engine)  
    return df  
  
def close_sprint(sprint_id):  
    engine = get_engine()  
    with engine.begin() as conn:  
        conn.execute(  
            text('''  
                UPDATE sprints  
                SET is_active = FALSE  
                WHERE id = :sprint_id  
            '''),  
            {'sprint_id': sprint_id}  
        )  
  
def get_sprint_tasks(sprint_id):  
    engine = get_engine()  
    query = text('SELECT * FROM tasks WHERE sprint_id = :sprint_id')  
    df = pd.read_sql_query(query, engine, params={'sprint_id': sprint_id})  
    return df  