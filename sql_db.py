import psycopg2

def connect(DATABASE_URL):
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def create_conversation_table(conn):
    execute_query(conn, create_conversation_table_query)

def execute_query(conn, query, args=()):
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()

#List of query strings
create_conversation_table_query = """
    CREATE TABLE IF NOT EXISTS
        conversation
    (greeting text unique, response text)
"""