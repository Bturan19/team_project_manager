from sqlalchemy import text  
from src.db import get_engine  
  
def initialize_database():  
    engine = get_engine()  
    with engine.begin() as conn:  
        # Create projects table  
        conn.execute(text('''  
            CREATE TABLE IF NOT EXISTS projects (  
                id SERIAL PRIMARY KEY,  
                name VARCHAR(255) NOT NULL UNIQUE,  
                description TEXT,  
                start_date DATE,  
                estimated_end_date DATE,  
                color VARCHAR(10),  
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
            );  
        '''))  
  
        # Create sprints table  
        conn.execute(text('''  
            CREATE TABLE IF NOT EXISTS sprints (  
                id SERIAL PRIMARY KEY,  
                name VARCHAR(255) NOT NULL,  
                start_date DATE,  
                end_date DATE,  
                is_active BOOLEAN DEFAULT TRUE,  
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
            );  
        '''))  
  
        # Create tasks table  
        conn.execute(text('''  
            CREATE TABLE IF NOT EXISTS tasks (  
                id SERIAL PRIMARY KEY,  
                title VARCHAR(255) NOT NULL,  
                description TEXT,  
                status VARCHAR(50) NOT NULL,  
                tags TEXT,  
                project_id INTEGER REFERENCES projects(id),  
                sprint_id INTEGER REFERENCES sprints(id),  
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
            );  
        '''))  
  
        # Create knowledge_base table  
        conn.execute(text('''  
            CREATE TABLE IF NOT EXISTS knowledge_base (  
                id SERIAL PRIMARY KEY,  
                title VARCHAR(255) NOT NULL,  
                content TEXT NOT NULL,  
                tags TEXT,  
                project_id INTEGER REFERENCES projects(id),  
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
            );  
        '''))  