from utils.db import get_db_connection

def execute_query(sql):
    """
    Executes the provided SQL query and returns the result as a list of dictionaries.
    If execution fails, returns an empty list and prints the error.
    """
    try:
        print("📥 Executing SQL:")
        print(sql)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        print("❌ Error executing query:")
        print("* Exception:", e)
        results = []
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

    return results

