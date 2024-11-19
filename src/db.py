# src/db.py
import os
import sqlite3
import streamlit as st  
from pathlib import Path
from sqlalchemy import create_engine  

# Define the path to the database file
DB_PATH = Path(__file__).parent.parent / "data" / "task_manager.db"
DB_PATH = "/tmp/task_manager.db"

def get_engine():  
    # Get the DATABASE_URL from environment variables  
    DATABASE_URL = st.secrets["database"]["url"] 
  
    # Create the engine  
    engine = create_engine(DATABASE_URL)  
    return engine  

def get_connection():
    #conn = sqlite3.connect(DB_PATH)
    engine = get_engine()  
    conn = engine.connect() 
    return conn