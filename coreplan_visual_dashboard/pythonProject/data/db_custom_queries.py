import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def get_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)

def load_performance_data():
    engine = get_engine()
    query = "SELECT * FROM employee_performance"
    return pd.read_sql(query, engine)

def load_financial_data():
    engine = get_engine()
    query = "SELECT * FROM financial_data"
    return pd.read_sql(query, engine)

def load_planning_data():
    engine = get_engine()
    query = "SELECT * FROM resource_planning"
    return pd.read_sql(query, engine)

def load_reporting_data():
    engine = get_engine()
    query = "SELECT * FROM reporting_data"
    return pd.read_sql(query, engine)

def load_departments():
    engine = get_engine()
    query = "SELECT * FROM departments"
    return pd.read_sql(query, engine)
