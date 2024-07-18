import sys
import os
import mariadb
from dotenv import load_dotenv
load_dotenv()
# def runQuery(conn: (), query: string) -> string:
def queries(conn: object, query: str)->str:
    """
    Function for executing SQL queries on a MariaDB database.

    Args:
        conn (dict): dictionary containing the connection parameters for the database.
        query (str): SQL query to be executed.

    Returns:
        list or None: A list of tuples containing the result rows if the query is a SELECT or DESCRIBE statement. #pylint: disable=line-too-long
                      None for other query types (e.g., CREATE, INSERT, etc.), which will print "Done" on success. #pylint: disable=line-too-long
    
    Raises:
        SystemExit: If there is an error connecting to the database, the program will exit.
        mariadb.Error: If there is an error executing the SQL query, it will be printed.
        Exception: If there is any unexpected error, it will be printed.
    """
    try:
        conn = mariadb.connect(**conn)
   #   print(type(conn))
    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)
    finally:
    #Connecting cursor to variable cur
        cur = conn.cursor()
    try:
        cur.execute("USE new;")
        cur.execute(query)
        conn.commit()
        if query.strip().lower().startswith(("select", "describe")):
            row = cur.fetchall()
        else:
            print("Done")
            row = None
    except mariadb.Error as e:
        print(f"SQL error: {e}")
        row = None
    except Exception as e:
        print(f"Unexpected error: {e}")
        row = None
    finally:
 #Closing connection
        cur.close()
        conn.close()
    return row
sql_commands = {
    #Deleting the table projects
    "drop": "DROP TABLE projects;",
    #Creating a table projects
    "create": """
    CREATE TABLE projects (
    project_id INT,
    project_name VARCHAR(255) NOT NULL,
    begin_date DATE,
    end_date DATE,
    cost DECIMAL(15,2) NOT NULL
    );""",
    #Inserting rows of values to the table
    "insert": """INSERT INTO projects VALUES (2, 'second', '2012-02-01', '2012-02-02', 75),
    (1, 'first', '2012-02-02', '2012-03-02', 50),
    (3, 'third', '2012-03-02', '2012-04-02', 100);""",
    #Adding a new column called Incharge
    "add_column": "ALTER TABLE projects ADD incharge VARCHAR(255);",
    #Updating project_id as primary key
    "primary_key": "ALTER TABLE projects ADD PRIMARY KEY (project_id);",
    #Adding the values to the new column incharge
    "update": "UPDATE projects SET incharge='Prateek' WHERE project_id=1;",
    #Printing the table content in descending order
    "select_desc": "SELECT * FROM projects ORDER BY project_id DESC;",
    #Displaying the minimum amount in the cost column
    "select_min": "SELECT MIN(cost) FROM projects;",
    #Displaying the columns incharge and project_id only
    "select_specific": "SELECT incharge AS Contactperson, project_id AS ID FROM projects;",
    #Deleting a column
    "delete_column": "ALTER TABLE projects DROP COLUMN begin_date;",
    #Selecting all the data
    "select_all": "SELECT * FROM projects;",
    #Description of the table
    "describe": "DESCRIBE projects;"
}
# Prompt user for input
user_input = input("Enter the function you want to perform: ")
query_input= sql_commands.get(user_input)
if query_input:
    conn_cred = {
        'host': os.getenv("HOST"),
        'user': os.getenv("MYSQL_USER"),
        'password': os.getenv("MYSQL_PASSWORD")
    }

    res_row = queries(conn_cred, query_input)
    if res_row:
        for row in res_row:
            print(row)
else:
    print("Invalid function input. Please choose a valid SQL command.")