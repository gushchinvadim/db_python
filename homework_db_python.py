
import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email VARCHAR(40) NOT NULL,
            phones DECIMAL
            );
            """)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client_phone(
            client_id INTEGER NOT NULL REFERENCES client(id),
            phones DECIMAL
            );
            """)
        conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client(first_name, last_name, email, phones)
            VALUES (%s,%s,%s,%s);""",
            (first_name, last_name, email, phones))
        conn.commit()
#
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client_phone(client_id, phones)
            VALUES (%s,%s);""",
            (client_id, phone))
        conn.commit()
def change_client(conn, id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE client SET first_name=%s, last_name=%s, email=%s, phones=%s WHERE id=%s;
            """, (first_name,last_name, email,phones, id))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())
        conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client_phone WHERE client_id=%s and phones=%s;
            """, (client_id, phone))
        conn.commit()

def delete_client(conn, client_id, id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client_phone WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
            DELETE FROM client WHERE id=%s;
            """, (id,))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT first_name, last_name FROM client WHERE first_name = %s or last_name = %s or email = %s ;
        """, (first_name,last_name, email))

        print(cur.fetchall())

with psycopg2.connect(database="postgres", user="postgres", password="postgres") as conn:

    # create_db(conn)
    # add_client(conn,'Иван','Солярка', 'ivsol@test.com', )
    # add_client(conn, 'Иван', 'Иванов', 'ivaiva@test.com', 98753654422)
    # add_client(conn, 'Петр', 'Петров', 'petrp@test.com', 44473654422)
    # add_phone(conn,1,44473654422)
    # add_phone(conn, 2, 98753654422)
    # add_phone(conn, 3, 89456780987)
    # change_client(conn,1,'Gena','Gurin','gena@kjh.com')
    # change_client(conn, 2, 'Vasja', 'Pupkin', 'vpuk@kjh.com', 8937636366)
    # delete_phone(conn, 2, 98753654422)
    # delete_phone(conn, 1, 44473654422)
    # delete_phone(conn, 3, 89456780987)
    # delete_client(conn,1, 1)
    # delete_client(conn,2, 2)
    # find_client(conn,None,None,'ivaiva@test.com')
    # find_client(conn, 'Петр', None, None)

conn.close()