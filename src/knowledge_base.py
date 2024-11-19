# src/knowledge_base.py  
import pandas as pd  
from src.db import get_engine  
from sqlalchemy import text  
  
def add_knowledge_entry(title, content, tags, project_id):  
    engine = get_engine()  
    with engine.begin() as conn:  
        conn.execute(  
            text('''  
                INSERT INTO knowledge_base (title, content, tags, project_id)  
                VALUES (:title, :content, :tags, :project_id)  
            '''),  
            {  
                'title': title,  
                'content': content,  
                'tags': tags,  
                'project_id': project_id  
            }  
        )  
  
def get_all_knowledge_entries():  
    engine = get_engine()  
    query = text('''  
        SELECT knowledge_base.*, projects.name AS project_name  
        FROM knowledge_base  
        LEFT JOIN projects ON knowledge_base.project_id = projects.id  
    ''')  
    df = pd.read_sql_query(query, engine)  
    return df  