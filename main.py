import psycopg2


def conn_db(conn):
    with conn.cursor() as cur:
        cur.execute("""                       
            create table if not exists Last_name (
	        id serial primary key,
	        name varchar(60)
            );
            
            create table if not exists First_name (
	        id integer primary key references Last_name(id),
	        name varchar(120)
	        );


            create table if not exists Mail (
	        id integer primary key references Last_name(id),
	        name varchar(120)
            );


            create table if not exists Number (
	        id SERIAL primary key,
	        name varchar(120),
	        last_name_id integer not null references Last_name(id)
            );
            """)
        conn.commit()
    conn.close

def drop_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE Number;
            DROP TABLE Mail;
            DROP TABLE First_name;
            DROP TABLE Last_name 
            """)
        conn.commit()
    conn.close

def add_client(conn, last_name, first_name, mail):
    with conn.cursor() as cur:
        cur.execute("""
            insert into last_name(name)
            values (%s); 
            """, (last_name,))
        def get_id(name):
            cur.execute("""select id from last_name where name = (%s)""", (name,))
            return cur.fetchone()[0]
        last_name_id = get_id(last_name)
        cur.execute("""
            insert into first_name(id, name)
            values ((%s), (%s)); 
            """, (last_name_id, first_name))
        cur.execute("""
            insert into mail(id, name)
            values ((%s), (%s))
            """, (last_name_id, mail))
        conn.commit()
    conn.close

def add_phone(conn, last_name, number):
    with conn.cursor() as cur:
        def get_id(name):
            cur.execute("""select id from last_name where name = (%s)""", (name,))
            return cur.fetchone()[0]
        last_name_id = get_id(last_name)
        cur.execute("""
            insert into number(name, last_name_id)
            values ((%s), (%s));
            """, (number, last_name_id))
        conn.commit()
    conn.close

def change_client(conn, last_name=None, first_name=None, mail=None)
    with conn.cursor() as cur:
        cur.execute("""
                UPDATE course SET name=%s WHERE id=%s;
                """, (last_name, python_id))
        cur.execute("""
        SELECT * FROM course;
        """)
        print(cur.fetchall())

with psycopg2.connect(database="test_new", user="postgres", password="129414") as conn:
    add_phone(conn, 'Kerzhakov', '891512454678')


