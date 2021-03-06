import psycopg2
import os

from lists import default_commands, heroes, full_hero_list, strength, agility, intelligence

DB = os.environ['DATABASE_URL']

# For when the time comes to implement dota api stuff
# https://steamcommunity.com/dev/registerkey



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
def fetch_two_query(query, args=()):
    try:
        conn = connect(DB)
        cur = conn.cursor()
        cur.execute(query, args)
        results = [list(i) for i in cur.fetchall()]
        close(conn, cur)
        return [(i[0],i[1]) for i in results]
    except Exception as e:
        print(f'***Error: {e} handling query: {query}')




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





### CONVERSATION TABLE FUNCTIONS ###

def create_conversation_table():
    execute_query(create_conversation_table_query)

def append_conversation_table(greeting, response, creator_id):
    execute_query(append_conversation_table_query, (greeting, response, creator_id))

def fetch_all_greetings():
    return fetch_query(select_greetings) 

def response(greeting):
    return fetch_query(select_response, (greeting,))

def delete_greeting(greeting, user_id, master_id):
    check_id = fetch_query(get_creator_id, (greeting,))
    print(f"found check_id {check_id}")
    if str(user_id) in [check_id[0], str(master_id)]:
        print(f"Attempting to delete {greeting}")
        execute_query(delete_greeting_query, (greeting,))
        return 1




############################
### DOTA TABLE FUNCTIONS ###
############################

# INITIAL TABLE CREATION AND INSERTION OF DEFAULT VALUES
def create_dota_tables():

    # For a fresh start, drops all tables and also resets the auto increment IDs.
    # print("Wiping all dota tables.")
    # execute_query(delete_pools_table_query)
    # execute_query(delete_user_table_query)
    # execute_query(delete_hero_table_query)

    # execute_query(reset_increments_hero_table_query)
    # execute_query(reset_increments_user_table_query)
    
    #Create Hero table and fill with hero names
    print("Creating hero table.")
    execute_query(create_hero_table_query)
    for hero in full_hero_list:
        print(f"Adding {hero} to the dota_heroes table.")
        execute_query(append_hero_table_query, (hero, 0))
    
    # Create pools table and fill with the default 3 attribute pools
    print("Creating user pools table.")
    execute_query(create_user_pools_query)
    execute_query(append_user_pools_query, ('Strength','default'))
    execute_query(append_user_pools_query, ('Agility','default'))
    execute_query(append_user_pools_query, ('Intelligence','default'))

    # Create user table
    print("Creating hero-pool pairs table.")
    execute_query(create_hero_pools_query)
    for hero in strength:
        execute_query(append_hero_pools_query, {'pool_id':get_pool_id('Strength'), 'hero_id':get_hero_id(hero)})
        print(f"Adding {hero} of id: {get_hero_id(hero)} to pool 'Strength' of id: {get_pool_id('Strength')}")
    for hero in agility:
        execute_query(append_hero_pools_query, {'pool_id':get_pool_id('Agility'), 'hero_id':get_hero_id(hero)})
        print(f"Adding {hero} of id: {get_hero_id(hero)} to pool 'Agility' of id: {get_pool_id('Agility')}")
    for hero in intelligence:
        execute_query(append_hero_pools_query, {'pool_id':get_pool_id('Intelligence'), 'hero_id':get_hero_id(hero)})
        print(f"Adding {hero} of id: {get_hero_id(hero)} to pool 'Intelligence' of id: {get_pool_id('Intelligence')}")
    
    print("Success...?!")



# POOL & USER FUNCTIONS

def get_all_pools():
    pools = fetch_query(get_pools_query)
    if pools != None:
        pools = (str(pools)[1:-1]).replace("'", "")
    return pools

def get_pool_id(pool_name):
    id = fetch_query(get_pool_id_query, (pool_name,))
    return id[0]

def get_users():
    return fetch_query(get_users_query)

def get_users_pools(user_id):
    pools = fetch_query(get_user_pools_query, (user_id,))
    if pools != 'None':
        pools = (str(pools)[1:-1]).replace("'","").title()
    return pools

def delete_pool(pool, user_id, master_id):
    pool_id = get_pool_id(pool)
    check_id = fetch_query(get_user_id, (pool_id,))
    if str(user_id) in [check_id[0], str(master_id)]:
        print(f"Attempting to delete {pool} of id {pool_id}")
        execute_query(delete_from_hero_pools_query, (pool_id,))
        execute_query(delete_pool_query, (pool_id,))
        return 1



# HERO FUNCTIONS

def findhero(hero):
    if hero.upper() in heroes.keys():
        return heroes[hero.upper()]
    else:
        return "ERROR"

def get_hero_id(hero):
    hero = findhero(hero)
    id = fetch_query(get_hero_id_query, (hero,))
    return id[0]

def get_hero_name(hero_id):
    return fetch_query(get_hero_name_query, (hero_id,))

def select_heroes_from_pool(pool_name):
    pool_id = get_pool_id(pool_name)
    hero_ids = fetch_query(select_heroes_from_pool_query, (pool_id,))
    heroes_in_pool = [get_hero_name(hero_id)[0] for hero_id in hero_ids]
    return ", ".join(heroes_in_pool)

def add_hero_to_pool(hero_name, pool_name):
    hero_id = get_hero_id(hero_name)
    pool_id = get_pool_id(pool_name)
    execute_query(append_hero_pools_query, {'pool_id':pool_id, 'hero_id':hero_id})



# HERO SCORE FUNCTIONS

def get_hero_score(hero):
    hero_id = get_hero_id(hero)
    return fetch_query(get_hero_score_query, (int(hero_id),))

def get_scores(count, top_or_bottom):
    if top_or_bottom == 'TOP':
        return fetch_two_query(get_top_scores_query, (int(count),))
    else:
        return fetch_two_query(get_bottom_scores_query, (int(count),))

def change_hero_score(hero_id, plus_or_minus):
    print(f"Attempting to lookup {hero_id} and {plus_or_minus}")
    if plus_or_minus == "ADD":
        execute_query(add_hero_score_query, (hero_id,))
    elif plus_or_minus == "SUB":
        execute_query(subtract_hero_score_query, (hero_id,))

def reset_score(hero_to_reset):
    execute_query(reset_score_query, (get_hero_id(hero_to_reset),))

def reset_all_scores():
    execute_query(reset_all_scores_query)





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




##########################
### DOTA TABLE QUERIES ###
##########################

#DELETING TO WIPE CLEAN WHILE BUILDING
delete_hero_table_query = """
    DROP TABLE
        dota_heroes"""
delete_user_table_query = """
    DROP TABLE
        user_pools"""
delete_pools_table_query = """
    DROP TABLE
        hero_pools"""


#RESETTING AUTO INCREMENT IDS
reset_increments_hero_table_query = """
    ALTER SEQUENCE 
        dota_heroes_hero_id_seq 
    RESTART WITH 1"""
reset_increments_user_table_query = """
    ALTER SEQUENCE 
        user_pools_pool_id_seq 
    RESTART WITH 1"""


#INITIAL TABLE CREATION
create_hero_table_query = """
    CREATE TABLE IF NOT EXISTS
        dota_heroes
    (hero_id SERIAL PRIMARY KEY, hero_name text, score int, UNIQUE(hero_name))"""
create_user_pools_query = """
    CREATE TABLE IF NOT EXISTS
        user_pools
    (pool_id SERIAL PRIMARY KEY, pool_name text, user_id text, UNIQUE(pool_name))"""
create_hero_pools_query = """
    CREATE TABLE IF NOT EXISTS
        hero_pools
    (pool_id int, hero_id int, 
    FOREIGN KEY (pool_id) REFERENCES user_pools(pool_id), 
    FOREIGN KEY (hero_id) REFERENCES dota_heroes(hero_id))"""


# APPEND TABLE QUERIES
append_hero_table_query = """
    INSERT INTO
        dota_heroes (hero_name,score)
    VALUES
        (%s, %s)
    ON CONFLICT DO NOTHING"""
append_user_pools_query = """
    INSERT INTO
        user_pools (pool_name, user_id)
    VALUES
        (%s, %s)
    ON CONFLICT DO NOTHING"""
append_hero_pools_query = """
    INSERT INTO
        hero_pools (pool_id, hero_id)
    SELECT
        %(pool_id)s, %(hero_id)s
    WHERE NOT EXISTS
        (SELECT
            *
        FROM
            hero_pools
        WHERE
            pool_id=%(pool_id)s AND hero_id=%(hero_id)s)"""



#DELETE QUERIES FOR USERS
delete_pool_query = """
    DELETE FROM
        user_pools
    WHERE
        pool_id=%s"""
delete_from_hero_pools_query = """
    DELETE FROM
        hero_pools
    WHERE
        pool_id=%s"""
delete_hero_from_pool_query = """
    DELETE FROM
        hero_pools
    WHERE
        pool_id=%(pool_id)s AND hero_id=%(hero_id)s"""



# VARIED SELECT QUERIES
get_pool_id_query = """
    SELECT
        pool_id
    FROM 
        user_pools
    WHERE
        pool_name=%s"""
get_pools_query = """
    SELECT DISTINCT
        pool_name
    FROM
        user_pools"""

get_users_query = """
    SELECT DISTINCT
        user_id
    FROM
        user_pools"""
get_user_pools_query = """
    SELECT DISTINCT
        pool_name
    FROM
        user_pools
    WHERE
        user_id=%s"""
get_user_id = """
    SELECT 
        user_id
    FROM
        user_pools
    WHERE
        pool_id=%s"""

get_hero_name_query = """
    SELECT
        hero_name
    FROM
        dota_heroes
    WHERE
        hero_id=%s"""
get_hero_id_query = """
    SELECT 
        hero_id
    FROM
        dota_heroes
    WHERE
        hero_name=%s"""
select_heroes_from_pool_query = """
    SELECT
        hero_id
    FROM
        hero_pools
    WHERE
        pool_id=%s"""



# HERO SCORE QUERIES
get_hero_score_query = """
    SELECT
        score
    FROM
        dota_heroes
    WHERE
        hero_id=%s"""
add_hero_score_query = """
    UPDATE
        dota_heroes
    SET
        score = score + 1
    WHERE
        hero_id=%s
"""
subtract_hero_score_query = """
    UPDATE
        dota_heroes
    SET
        score = score - 1
    WHERE
        hero_id=%s
"""
get_top_scores_query = """
    SELECT
        hero_name, score
    FROM
        dota_heroes
    ORDER BY
        score DESC
    FETCH FIRST %s ROWS ONLY"""
get_bottom_scores_query = """
    SELECT
        hero_name, score
    FROM
        dota_heroes
    ORDER BY
        score ASC
    FETCH FIRST %s ROWS ONLY"""
reset_score_query = """
    UPDATE
        dota_heroes
    SET
        score = 0
    WHERE
        hero_id=%s
"""
reset_all_scores_query = """
    UPDATE
        dota_heroes
    SET
        score = 0
"""