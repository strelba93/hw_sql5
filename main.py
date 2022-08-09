import psycopg2


def conn_db(conn):
    with conn.cursor() as cur:
        cur.execute("""                       
            create table if not exists Client_id (
	        id SERIAL primary key,
	        first_name varchar(80),
	        last_name varchar(80),
	        mail varchar(80)
	        );

            create table if not exists Number (
	        id SERIAL primary key,
	        data varchar(120),
	        client_id integer not null references Client_id(id)
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

def add_client(conn, first_name, last_name, mail):
    with conn.cursor() as cur:
        cur.execute("""
            insert into client_id(first_name, last_name, mail)
            values ((%s), (%s), (%s))
            """, (first_name, last_name, mail))
        conn.commit()
    conn.close

def add_phone(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
            insert into number(data, client_id)
            values ((%s), (%s))
            """, (client_id, number))
        conn.commit()
    conn.close

def change_client (conn, client_id, first_name=None, last_name=None, mail=None):
    with conn.cursor() as cur:
        def info():
            cur.execute("""
                select first_name, last_name, mail from Client_id
                where id = (%s);
                """, (client_id,))
            return (cur.fetchall(), 'Client changed')
        if first_name != None and last_name == None and mail == None:
            cur.execute("""
                UPDATE Client_id SET first_name=%s WHERE id=%s;
                """, (first_name, client_id))
            print(info())
        elif first_name != None and last_name != None and mail == None:
            cur.execute("""
                UPDATE Client_id SET first_name=%s, last_name=%s 
                WHERE id=%s;
                """, (first_name, last_name, client_id))
            print(info())
        elif first_name != None and last_name != None and mail != None:
            cur.execute("""
                UPDATE Client_id SET first_name=%s, last_name=%s, mail=%s 
                WHERE id=%s;
                """, (first_name, last_name, mail, client_id))
            print(info())
        else:
            print('Client not changed')

def select_phone(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            select data from number where client_id = (%s);
            """, (client_id,))
        return cur.fetchall()

def delete_phone(conn, phone):
    def get_id():
        with conn.cursor() as cur:
            cur.execute("""
                select id from number
                where data=%s;
                """, (phone,))
            return cur.fetchone()[0]
    phone_id = get_id()
    with conn.cursor() as cur:
        cur.execute("""
            delete from number 
            WHERE id=%s;
            """, (phone_id,))
        conn.commit()
    conn.close

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            delete from client_id 
            WHERE id=%s;
            """, (client_id,))
        conn.commit()
    conn.close

def find_client(conn, first_name=None, last_name=None, mail=None, number=None):
    with conn.cursor() as cur:
        if first_name != None:
            cur.execute("""
                select ci.id, ci.first_name, ci.last_name, n.data from client_id ci
                join number n on ci.id = n.client_id 
                where ci.first_name = %s;
                """, (first_name,))
            return cur.fetchall()
        elif last_name != None:
            cur.execute("""
                select ci.id, ci.first_name, ci.last_name, n.data from client_id ci
                join number n on ci.id = n.client_id 
                where ci.last_name = %s;
                """, (last_name,))
            return cur.fetchall()
        elif mail != None:
            cur.execute("""
                select ci.id, ci.first_name, ci.last_name, n.data from client_id ci
                join number n on ci.id = n.client_id 
                where mail = %s;
                """, (mail,))
            return cur.fetchall()
        elif number != None:
            cur.execute("""
                select ci.id, ci.first_name, ci.last_name, n.data from client_id ci
                join number n on ci.id = n.client_id 
                where n.data = %s;
                """, (number,))
            return cur.fetchall()
        else:
            print('Client not found')


with psycopg2.connect(database="db_test", user="postgres", password="129414") as conn:
    # conn_db(conn)
    # add_client(conn, 'Paul', 'Sholes', "sholes@mail")
    # add_client(conn, 'David', 'Beckham', 'becks7@gmal.com')
    # add_client(conn, 'Rio', 'Ferdinand', 'ferdinand@post')
    # add_client(conn, 'Thierry', 'Henry', 'henry@mail')
    # add_phone(conn, '89165546541', 1)
    # add_phone(conn, '89165123132', 1)
    # add_phone(conn, '89165544561', 3)
    # change_client(conn, 1, 'Sholesss', 'Paulsss', 'sholes@mail.comssss')
    # delete_phone(conn, '89165546541')
    # print(select_phone(conn, 1))
    # delete_client(conn, 3)





