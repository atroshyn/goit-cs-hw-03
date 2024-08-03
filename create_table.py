import psycopg2
from psycopg2 import Error
from contextlib import contextmanager
from config import *

@contextmanager
def create_connection():
    """ create a database connection to a PostgreSQL database """
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        conn.close()

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)

if __name__ == '__main__':
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
     id SERIAL PRIMARY KEY,
     fullname VARCHAR(100) NOT NULL,
     email VARCHAR(100) UNIQUE
     );
    """

    sql_create_statuses_table = """
    CREATE TABLE IF NOT EXISTS statuses (
     id SERIAL PRIMARY KEY, 
     name VARCHAR(50) UNIQUE
    );
    """

    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
     id SERIAL PRIMARY KEY, 
     title VARCHAR(100),
     description text,
     status_id INTEGER,
     FOREIGN KEY (status_id) REFERENCES statuses (id),
     user_id INTEGER,
     FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """

    with create_connection() as conn:
        if conn is not None:
			# create users table
            create_table(conn, sql_create_users_table)

			# create statuses table
            create_table(conn, sql_create_statuses_table)

			# create tasks table
            create_table(conn, sql_create_tasks_table)
        else:
            print("Error! cannot create the database connection.")
