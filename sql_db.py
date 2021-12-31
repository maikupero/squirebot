import psycopg2

def connect(DATABASE_URL):
    return psycopg2.connect(DATABASE_URL, sslmode='require')