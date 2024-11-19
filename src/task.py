# src/task.py  
import pandas as pd  
from src.db import get_engine  
from sqlalchemy import text  
  
def create_task(title, description, status, tags, project_id, sprint_id=None):  
    engine = get_engine()  
    with engine.begin() as conn:  
        try:  
            conn.execute(  
                text('''  
                    INSERT INTO tasks (title, description, status, tags, project_id, sprint_id)  
                    VALUES (:title, :description, :status, :tags, :project_id, :sprint_id)  
                '''),  
                {  
                    'title': title,  
                    'description': description,  
                    'status': status,  
                    'tags': tags,  
                    'project_id': project_id,  
                    'sprint_id': sprint_id  
                }  
            )  
        except Exception as e:  
            print(f"Error inserting task: {e}")  
  
def get_all_tasks():  
    engine = get_engine()  
    query = text('''  
        SELECT tasks.*, projects.name AS project_name, projects.color AS project_color, sprints.name AS sprint_name  
        FROM tasks  
        LEFT JOIN projects ON tasks.project_id = projects.id  
        LEFT JOIN sprints ON tasks.sprint_id = sprints.id  
    ''')  
    df = pd.read_sql_query(query, engine)  
    return df  
  
def update_task(task_id, title, description, status, tags, project_id, sprint_id=None):  
    engine = get_engine()  
    with engine.begin() as conn:  
        try:  
            conn.execute(  
                text('''  
                    UPDATE tasks  
                    SET title = :title, description = :description, status = :status, tags = :tags,  
                        project_id = :project_id, sprint_id = :sprint_id  
                    WHERE id = :task_id  
                '''),  
                {  
                    'title': title,  
                    'description': description,  
                    'status': status,  
                    'tags': tags,  
                    'project_id': project_id,  
                    'sprint_id': sprint_id,  
                    'task_id': task_id  
                }  
            )  
        except Exception as e:  
            print(f"Error updating task: {e}")  
  
def delete_task(task_id):  
    engine = get_engine()  
    with engine.begin() as conn:  
        conn.execute(  
            text('DELETE FROM tasks WHERE id = :task_id'),  
            {'task_id': task_id}  
        )  