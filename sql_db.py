import psycopg2
import os
DB = os.environ['DATABASE_URL']

# BASE COMMANDS FOR CONNECTION AND QUERIES
def connect(DB):
    return psycopg2.connect(DB, sslmode='require')

def close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def execute_query(query, args=()):
    try:
        conn = connect(DB)
        cur = conn.cursor()
        print(query)
        cur.execute(query, args)
        close(conn, cur)
    except Exception as e:
        print(f'***Error: {e} handling query: {query}')

def fetch_query(query, args=()):
    try:
        conn = connect(DB)
        cur = conn.cursor()
        cur.execute(query, args)
        results = [list(i) for i in cur.fetchall()]
        close(conn, cur)
        return [i[0] for i in results]
    except Exception as e:
        print(f'***Error: {e} handling query: {query}')



# INITIAL TABLE CREATION AND FILL WITH DEFAULT VALUES
def create_command_table():
    execute_query(create_command_table_query)
    default_commands = ['hi','help','attend','weather','dota','dotes','dop','doto','guess','aoe','delete']
    for command in default_commands:
        execute_query(default_command_table_query, args={'command':command})

def create_conversation_table():
    execute_query(create_conversation_table_query)
    execute_query(default_conversation_table_query)



# APPENDING TO EXISTING TABLES
def append_command_table(command):
    execute_query(append_command_table_query, args={'command':command})
def append_conversation_table(greeting, response):
    execute_query(append_conversation_table_query, args={'greeting':greeting, 'response':response})


# DELETING ROW OR ROWS
def get_column(table):
    return str(fetch_query(get_column_query, args={'table':table}))[2:-2]
def delete_row(table, row):
    print(f"Attempting to delete {row} from {table}.")
    print(f"Getting first column of {table}: {get_column(table)}")
    execute_query(delete_row_query, args={'table':table, 'table':get_column(table), 'row':row})
        
# CHECKING AND RETURNING VALUES IN EXISTING TABLES
def fetch_tables():
    return fetch_query(select_tables)
def fetch_all_columns(table):
    return fetch_query(select_all_columns, args={'table':table})
def fetch_all_rows(table):
    print(f"trying to fetch all rows from {table}.")
    return fetch_query(select_all_rows, args={'table':table})

# SELECT QUERIES
def commands():
    return fetch_query(select_commands)
def greetings():
    return fetch_query(select_greetings) 
def response(greeting):
    return fetch_query(select_response, args={'greeting':greeting})


#GENERAL QUERIES
select_all_rows = """
    SELECT
        *
    FROM
        %(table)s
"""
select_all_columns = """
    SELECT 
        column_name
    FROM 
        information_schema.columns 
    WHERE 
        table_name= N'%(table)s'
"""
select_tables = """
    SELECT 
        Table_name
    FROM 
        information_schema.tables 
    WHERE 
        table_schema='public'
"""
get_column_query = """
    SELECT 
        column_name
    FROM 
        information_schema.columns 
    WHERE 
        table_name=N'%(table)s'
    LIMIT 1
"""
delete_row_query = """
    DELETE FROM
        %(table)s
    WHERE
        %(column)s = '%(row)s'
"""
2

# COMMAND TABLE QUERIES
create_command_table_query = """
    CREATE TABLE IF NOT EXISTS
        recognized_commands
    (commands text unique)
"""
default_command_table_query = """
    INSERT INTO
        recognized_commands
    VALUES
        %(command)s
    ON CONFLICT DO NOTHING
"""
append_command_table_query = """
    INSERT INTO
        recognized_commands
    VALUES
        %(command)s
    ON CONFLICT DO NOTHING
"""
select_commands = """
    SELECT
        commands
    FROM
        recognized_commands
"""

# CONVERSATION TABLE QUERIES
create_conversation_table_query = """
    CREATE TABLE IF NOT EXISTS
        conversation
    (greeting text unique, response text)
"""
default_conversation_table_query = """
    INSERT INTO
        conversation
    VALUES
        ('hi', 'hey!')
    ON CONFLICT DO NOTHING
"""
append_conversation_table_query = """
    INSERT INTO
        conversation
    VALUES
        (%(greeting)s, %(response)s)
    ON CONFLICT DO NOTHING
"""
select_greetings = """
    SELECT
        greeting
    FROM
        conversation
"""
select_response = """
    SELECT
        response
    FROM
        conversation
    WHERE
        greeting=%(greeting)s
"""