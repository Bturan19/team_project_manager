# src/project.py  
import pandas as pd  
from src.db import get_engine  
from sqlalchemy import text  
  
def create_project(name, description, start_date, estimated_end_date, color):  
    engine = get_engine()  
    with engine.begin() as conn:  
        conn.execute(  
            text('''  
                INSERT INTO projects (name, description, start_date, estimated_end_date, color)  
                VALUES (:name, :description, :start_date, :estimated_end_date, :color)  
            '''),  
            {  
                'name': name,  
                'description': description,  
                'start_date': start_date,  
                'estimated_end_date': estimated_end_date,  
                'color': color  
            }  
        )  
  
def update_project(project_id, name, description, start_date, estimated_end_date, color):  
    engine = get_engine()  
    with engine.begin() as conn:  
        try:  
            conn.execute(  
                text('''  
                    UPDATE projects  
                    SET name = :name, description = :description, start_date = :start_date,  
                        estimated_end_date = :estimated_end_date, color = :color  
                    WHERE id = :project_id  
                '''),  
                {  
                    'name': name,  
                    'description': description,  
                    'start_date': start_date,  
                    'estimated_end_date': estimated_end_date,  
                    'color': color,  
                    'project_id': project_id  
                }  
            )  
        except Exception as e:  
            print(f"Error updating project: {e}")  
  
def get_all_projects():  
    engine = get_engine()  
    query = text('SELECT * FROM projects')  
    df = pd.read_sql_query(query, engine)  
    return df  
  
def get_project_by_id(project_id):  
    engine = get_engine()  
    query = text('SELECT * FROM projects WHERE id = :project_id')  
    df = pd.read_sql_query(query, engine, params={'project_id': project_id})  
    return df  