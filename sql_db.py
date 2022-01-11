from discord.ext.commands.core import check
import psycopg2
import os
from psycopg2 import sql

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


### GENERAL FUNCTIONS ###
def fetch_tables():
    return fetch_query(select_tables)
select_tables = """
    SELECT 
        Table_name
    FROM 
        information_schema.tables 
    WHERE 
        table_schema='public'
"""
# query = sql.SQL("SELECT {field} FROM {table} WHERE {pkey} = %s").format(
#     field=sql.Identifier('my_name'),
#     table=sql.Identifier('some_table'),
#     pkey=sql.Identifier('id'))
#     sql.SQL("INSERT INTO {} VALUES (%s, %s)").format(sql.Identifier('my_table')), [10, 20])



### COMMAND TABLE FUNCTIONS ###
def create_command_table():
    execute_query(create_command_table_query)
    default_commands = ['hi','help','attend','weather','dota','dotes','dop','doto','guess','aoe',',randomciv','deletefrom', 'greetings', 'commands', 'tables']
    for command in default_commands:
        execute_query(append_command_table_query, (command,))

def append_command_table(command):
    execute_query(append_command_table_query, (command,))

def fetch_all_commands():
    return fetch_query(select_commands)

def delete_command(command):
    print(f"Attempting to delete {command}")
    execute_query(delete_command_query, (command,))

### COMMAND TABLE QUERIES ###
create_command_table_query = """
    CREATE TABLE IF NOT EXISTS
        recognized_commands
    (commands text unique)"""
append_command_table_query = """
    INSERT INTO
        recognized_commands
    VALUES
        (%s)
    ON CONFLICT DO NOTHING"""
select_commands = """
    SELECT
        commands
    FROM
        recognized_commands"""
delete_command_query = """
    DELETE FROM
        recognized_commands
    WHERE
        commands=%s"""
### CONVERSATION TABLE FUNCTIONS ###
def create_conversation_table():
    execute_query(create_conversation_table_query)
    execute_query(append_conversation_table_query, ('hi','hey!','default'))

def append_conversation_table(greeting, response, creator_id):
    execute_query(append_conversation_table_query, (greeting, response, creator_id))

def fetch_all_greetings():
    return fetch_query(select_greetings) 

def response(greeting):
    return fetch_query(select_response, (greeting,))

def delete_greeting(greeting, user_id, master_id):
    check_id = fetch_query(get_creator_id, (greeting,))
    print(f"checking user_id: ({type(user_id)}){user_id} against stored id: ({type(check_id)}){check_id}.") 
    if user_id == check_id or user_id == master_id:
        print(f"Attempting to delete {greeting}")
        execute_query(delete_greeting_query, (greeting,))
        return 1

### CONVERSATION TABLE QUERIES ###
create_conversation_table_query = """
    CREATE TABLE IF NOT EXISTS
        conversation
    (greeting text unique, response text, creator_id text)"""
append_conversation_table_query = """
    INSERT INTO
        conversation
    VALUES
        (%s, %s, %s)
    ON CONFLICT DO NOTHING"""
select_greetings = """
    SELECT
        greeting
    FROM
        conversation"""
select_response = """
    SELECT
        response
    FROM
        conversation
    WHERE
        greeting=%s"""
get_creator_id = """
    SELECT 
        creator_id
    FROM
        conversation
    WHERE
        greeting=%s"""
delete_greeting_query = """
    DELETE FROM
        conversation
    WHERE
        greeting=%s
"""


#GENERAL QUERIES
select_all_columns = """
    SELECT 
        column_name
    FROM 
        information_schema.columns 
    WHERE 
        table_name={}
"""

get_column_query = """
    SELECT 
        column_name
    FROM 
        information_schema.columns 
    WHERE 
        table_name={}
    LIMIT 1
"""
