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
    db_engine = os.getenv("DB_ENGINE")

    url = f"{db_engine}://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)


def load_performance_data():
    engine = get_engine()
    query = "SELECT * FROM employee_performance"
    df = pd.read_sql(query, engine)
    return df

def load_financial_data():
    engine = get_engine()
    query = """
        SELECT f.*, d.department_name
        FROM financial_data f
        JOIN departments d ON f.department_id = d.department_id
        WHERE d.department_name = 'Sales'
    """
    df = pd.read_sql(query, engine)
    return df

def load_planning_data():
    engine = get_engine()
    query = """
        SELECT rp.*, d.department_name
        FROM resource_planning rp
        JOIN departments d ON rp.department_id = d.department_id
        WHERE d.department_name = 'Sales'
    """
    df = pd.read_sql(query, engine)
    return df


def load_reporting_data():
    engine = get_engine()
    query = "SELECT * FROM reporting_data"
    df = pd.read_sql(query, engine)
    return df
