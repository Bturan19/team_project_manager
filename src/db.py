# src/db.py  
import streamlit as st  
from sqlalchemy import create_engine, text  
  
def get_engine():    
    # Get the DATABASE_URL from st.secrets  
    DATABASE_URL = st.secrets["database"]["url"]   
    # Create the engine  
    engine = create_engine(DATABASE_URL)    
    return engine  
  
def get_connection():  
    engine = get_engine()    
    conn = engine.connect()  
    return conn  