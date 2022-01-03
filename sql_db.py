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
        results = cur.fetchall()
        print(f"Found {results}, From Query: {query}")
        close(conn, cur)
        return (list(i) for i in results)
    except Exception as e:
        print(f'***Error: {e} handling query: {query}')

# INITIAL TABLE CREATION AND FILL WITH DEFAULT VALUES
def create_command_table():
    execute_query(create_command_table_query)
    default_commands = ['hi','help','attend','weather','dota','dotes','dop','doto','guess','aoe']
    for command in default_commands:
        print(f"Attempting to insert {command} into commands table.")
        execute_query(default_command_table_query(command))

def create_conversation_table():
    execute_query(create_conversation_table_query)
    execute_query(default_conversation_table_query)

# APPENDING TO EXISTING TABLES
def append_command_table(command):
    execute_query(append_command_table_query(command))
def append_conversation_table(greeting, response):
    execute_query(append_conversation_table_query(greeting, response))

# CHECKING AND RETURNING VALUES IN EXISTING TABLES
def commands():
    return fetch_query(select_commands)
    
def greetings():
    print("INITIATING GREETINGS QUERY")
    greetings = fetch_query(select_greetings)
    print(greetings)
    return greetings

def response(greeting):
    return fetch_query(select_response(greeting))

# DELETE COMMANDS FOR ROWS AND TABLES

# QUERIES FOR COMMAND TABLE
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
def append_command_table_query(command):
    return f"""
    INSERT INTO
        recognized_commands
    VALUES
        ('{command}')
"""
select_commands = """
    SELECT
        commands
    FROM
        recognized_commands
"""

# QUERIES FOR CONVERSATION TABLE
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
def append_conversation_table_query(greeting, response):
    return f"""
    INSERT INTO
        conversation
    VALUES
        ('{greeting}', '{response}')
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