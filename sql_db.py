import psycopg2
import os
from psycopg2 import sql
from lists import default_commands, heroes, hero_abbrevs, strength, agility, intelligence, stre, agil, inte

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



### COMMAND TABLE FUNCTIONS ###
def create_command_table():
    execute_query(create_command_table_query)
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
    if str(user_id) in [check_id[0], str(master_id)]:
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



### DOTA TABLE FUNCTIONS ###    
def create_dota_tables():
    #Start fresh
    print("Wiping all dota tables.")
    # execute_query(delete_hero_table_query)
    # execute_query(delete_user_table_query)
    # execute_query(delete_pools_table_query)

    #Create Hero table and fill with hero names
    print("Creating hero table.")
    execute_query(create_hero_table_query)
    for hero in heroes:
        print(f"Adding {hero} to the dota_heroes table.")
        execute_query(append_hero_table_query, (hero, 0))
    
    # Create pools table and fill with the default 3 attribute pools
    print("Creating user pools table.")
    execute_query(create_user_pools_query)
    execute_query(append_user_pools_query('strength','default'))
    execute_query(append_user_pools_query('agility','default'))
    execute_query(append_user_pools_query('intelligence','default'))

    # Create user table
    print("Creating hero-pool pairs table.")
    execute_query(create_hero_pools_query)
    for hero in strength:
        execute_query(append_hero_pools_query(1, get_hero_id(hero)))
        print(f"Adding {hero} of id: {get_hero_id(hero)} to pool 'strength' of id: {get_pool_id('strength')}")
    for hero in agility:
        execute_query(append_hero_pools_query(2, get_hero_id(hero)))
        print(f"Adding {hero} of id: {get_hero_id(hero)} to pool 'agility' of id: {get_pool_id('agility')}")
    for hero in intelligence:
        execute_query(append_hero_pools_query(3, get_hero_id(hero)))
        print(f"Adding {hero} of id: {get_hero_id(hero)} to pool 'intelligence' of id: {get_pool_id('intelligence')}")
    
    print("Success...?!")


def get_pool_id(pool_name):
    return fetch_query(get_pool_id_query(pool_name,))
def get_hero_id(hero):
    if hero in hero_abbrevs:
        hero = hero_abbrevs[hero]
    if hero.capitalize() in heroes:
        hero = hero.capitalize()
        return fetch_query(get_hero_id_query(hero,))
    else:
        return "Error"
def get_hero_score(hero):
    hero_id = get_hero_id(hero)
    return fetch_query(get_hero_score_query(hero_id,))
    
    

### DOTA TABLE QUERIES ###
#DELETING TO WIPE CLEAN WHILE BUILDING
delete_hero_table_query = """
    DELETE FROM
        dota_heroes"""
delete_user_table_query = """
    DELETE FROM
        dota_user_pools"""
delete_pools_table_query = """
    DELETE FROM
        hero_pools"""

#INITIAL CREATION
create_hero_table_query = """
    CREATE TABLE IF NOT EXISTS
        dota_heroes
    (hero_id SERIAL PRIMARY KEY, hero_name text, score int)"""
create_user_pools_query = """
    CREATE TABLE IF NOT EXISTS
        dota_user_pools
    (pool_id SERIAL PRIMARY KEY, pool_name text, user_id text)"""
create_hero_pools_query = """
    CREATE TABLE IF NOT EXISTS
        hero_pools
    (pool_id text, hero_id text, 
    FOREIGN KEY (pool_id) REFERENCES dota_user_pools(pool_id), 
    FOREIGN KEY (hero_id) REFERENCES dota_heroes(hero_id))"""

# FILL HERO TABLE QUERIES
append_hero_table_query = """
    INSERT INTO
        dota_heroes
    VALUES
        (%s, %s)
    ON CONFLICT DO NOTHING"""
# FILL HERO POOL DEFAULTS
append_user_pools_query = """
    INSERT INTO
        dota_user_pools
    VALUES
        (%s, %s)
    """
append_hero_pools_query = """
    INSERT INTO
        hero_pools
    VALUES
        (%s, %s)"""


get_pool_id_query = """
    SELECT
        pool_id
    FROM 
        dota_user_pools
    WHERE
        pool_name=%s"""
get_hero_id_query = """
    SELECT 
        hero_id
    FROM
        dota_heroes
    WHERE
        hero_name=%s"""
get_hero_score_query = """
    SELECT
        score
    FROM
        dota_heroes
    WHERE
        hero_id=%s"""



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