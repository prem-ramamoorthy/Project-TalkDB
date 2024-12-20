import mysql.connector
from mysql.connector import Error
def connect_to_database():
    file = open("Project-TalkDB\data_folder\dbdata.txt","r")
    data = file.read()
    data = eval(data)
    file.close()
    username = data['username']
    password = data['password']
    host = data['host']
    try:
        conn = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
        )
        if conn.is_connected():
            return conn
    except mysql.connector.Error as e:
        return None
def list_databases(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = [db[0] for db in cursor.fetchall()]
        return databases
    except mysql.connector.Error as e:
        return []

def list_tables(conn, database):
    try:
        cursor = conn.cursor()
        cursor.execute(f"USE {database};")
        cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in cursor.fetchall()]
        return tables
    except mysql.connector.Error as e:
        return []

def list_columns(conn, database, table):
    try:
        cursor = conn.cursor()
        cursor.execute(f"USE {database};")
        cursor.execute(f"DESCRIBE {table};")
        columns = [col[0] for col in cursor.fetchall()]
        return columns
    except mysql.connector.Error as e:
        return []

def main():
    conn = connect_to_database()
    if conn is None:
        return 
    try:
        data = {} 
        databases = list_databases(conn)
        if not databases:
            file2 = open("maindata.txt","w")
            file2.write("None")
            file2.close()
            return
        for db in databases:
            if db in ["information_schema", "mysql", "performance_schema", "sys"]:
                continue
            tables = list_tables(conn, db)
            if not tables:
                continue
            data[db] = {} 
            for table in tables:
                columns = list_columns(conn, db, table)
                data[db][table] = columns
        return data
    finally:
        if conn.is_connected():
            conn.close()

database_structure = main()
  
