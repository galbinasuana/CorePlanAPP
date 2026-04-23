import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Returns a live connection object to the MySQL database.
    Used for executing raw SQL through other modules.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

def run_query(sql):
    """
    Executes the given SQL string and returns the result as a list of dictionaries.
    Closes the connection automatically after execution.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        return []
    finally:
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except:
            pass
