import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_db_connection():
    """
    Create a database connection to the MySQL database specified by the db_name.

    Returns
    -------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        print("MySQL Database connection successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def execute_query(connection, query, data=None):
    """
    Execute a given SQL query on the provided database connection.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    query : str
        The SQL query to execute.
    data : tuple, optional
        The data tuple to pass to the query, for parameterized queries.

    Returns
    -------
    None
    """
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as e:
        print(f"The error '{e}' occurred")

def insert_category(connection, name, description):
    """
    Inserts a new category into the categories table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    name : str
        The name of the category.
    description : str
        The description of the category.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO categories (name, description)
    VALUES (%s, %s)
    """
    data = (name, description)
    execute_query(connection, query, data)

def insert_reporter(connection, name, email):
    """
    Inserts a new reporter into the reporters table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    name : str
        The name of the reporter.
    email : varchar
        The email of the reporter.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO reporters (name, email)
    VALUES (%s, %s)
    """
    data = (name, email)
    execute_query(connection, query, data)

def insert_publisher(connection, name, email):
    """
    Inserts a new publisher into the publishers table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    name : str
        The name of the publisher.
    email : varchar
        The email of the publisher.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO publishers (name, email)
    VALUES (%s, %s)
    """
    data = (name, email)
    execute_query(connection, query, data)

def insert_first(connection, category_id, reporter_id, publisher_id, datetime, title, body, link):
    """
    Inserts a new first article into the first table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    category_id : int
        The ID of the category.
    reporter_id : int
        The ID of the reporter.
    publisher_id : int
        The ID of the publisher.
    datetime : datetime
        The publication date and time of the first article.
    title : str
        The title of the first article.
    body : str
        The body text of the first article.
    link : str
        The URL link to the full first article.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO first (category_id, reporter_id, publisher_id, datetime, title, body, link)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    data = (category_id, reporter_id, publisher_id, datetime, title, body, link)
    execute_query(connection, query, data)

def insert_image(connection, first_id, image_url):
    """
    Inserts a new image into the images table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    first_id : int
        The ID of the first article associated with the image.
    image_url : str
        The URL of the image.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO images (first_id, image_url)
    VALUES (%s, %s)
    """
    data = (first_id, image_url)
    execute_query(connection, query, data)

def insert_summary(connection, first_id, summary_text):
    """
    Inserts a new summary into the summaries table.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    first_id : int
        The ID of the first article associated with the summary.
    summary_text : str
        The text of the summary.

    Returns
    -------
    None
    """
    query = """
    INSERT INTO summaries (first_id, summary_text)
    VALUES (%s, %s)
    """
    data = (first_id, summary_text)
    execute_query(connection, query, data)

# Example usage
if __name__ == "__main__":
    conn = create_db_connection()
    if conn is not None:
        insert_category(conn, "Politics", "All first related to politics")
        insert_category(conn, "Economics", "All first related to economics")
        insert_publisher(conn, "jonny" , "jonny@mial.com")
        
        # Add more insert calls for other tables
