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
        print([i[0] for i in results])
        return [i[0] for i in results]
    except Exception as e:
        print(f'***Error: {e} handling query: {query}')

# INITIAL TABLE CREATION AND FILL WITH DEFAULT VALUES
def create_command_table():
    execute_query(create_command_table_query)
    default_commands = ['hi','help','attend','weather','dota','dotes','dop','doto','guess','aoe','deletefrom']
    for command in default_commands:
        execute_query(default_command_table_query(command))

def create_conversation_table():
    execute_query(create_conversation_table_query)
    execute_query(default_conversation_table_query)

# APPENDING TO EXISTING TABLES
def append_command_table(command):
    execute_query(append_command_table_query(command))
def append_conversation_table(greeting, response):
    execute_query(append_conversation_table_query(greeting, response))

# DELETING ROW OR ROWS
def delete_row(table, rows=()):
    for row in rows:
        execute_query(delete_row_query(table, row))
        
# CHECKING AND RETURNING VALUES IN EXISTING TABLES
def fetch_tables():
    return fetch_query(select_tables)
def fetch_all_columns(table):
    return fetch_query(select_all_columns(table))
def fetch_all_rows(table):
    return fetch_query(select_all_rows(table))

def commands():
    return fetch_query(select_commands)

def greetings():
    return fetch_query(select_greetings) 

def response(greeting):
    return fetch_query(select_response(greeting))


# QUERIES FOR BUILDING COMMAND TABLE
create_command_table_query = """
    CREATE TABLE IF NOT EXISTS
        recognized_commands
    (commands text unique)
"""
def default_command_table_query(command):
    return f"""
    INSERT INTO
        recognized_commands
    VALUES
        ('{command}')
    ON CONFLICT DO NOTHING
"""


# QUERIES FOR BUILDING CONVERSATION TABLE
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

### APPEND QUERIES
def append_conversation_table_query(greeting, response):
    return f"""
    INSERT INTO
        conversation
    VALUES
        ('{greeting}', '{response}')
    ON CONFLICT DO NOTHING
"""
def append_command_table_query(command):
    return f"""
    INSERT INTO
        recognized_commands
    VALUES
        ('{command}')
    ON CONFLICT DO NOTHING
"""

### DELETE QUERIES 
### https://stackoverflow.com/questions/1054984/how-can-i-get-column-names-from-a-table-in-sql-server
def delete_row_query(table, row):
    return f"""
    DELETE FROM
        {table}
    WHERE
        (SELECT 
            column_name
        FROM 
            information_schema.columns 
        WHERE 
            table_name= N'{table}'
        LIMIT 1)={row}
"""

# OFFSET 1 ROWS   -- Skip this number of rows
# FETCH NEXT 1 ROWS ONLY;  -- Return this number of rows




### SELECT QUERIES ###
def select_all_rows(table):
    return f"""
    SELECT
        *
    FROM
        {table}
"""
def select_all_columns(table):
    return f"""
    SELECT 
        column_name
    FROM 
        information_schema.columns 
    WHERE 
        table_name= N'{table}'
"""

select_tables = """
    SELECT 
        Table_name
    FROM 
        information_schema.tables 
    WHERE 
        table_schema='public'
"""

select_commands = """
    SELECT
        commands
    FROM
        recognized_commands
"""
select_greetings = """
    SELECT
        greeting
    FROM
        conversation
"""
def select_response(greeting):
    return f"""
    SELECT
        response
    FROM
        conversation
    WHERE
        greeting="{greeting}"
"""