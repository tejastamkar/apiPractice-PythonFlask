import sqlite3







def createDb(): 
    conn = sqlite3.connect("books.sqlite")
    cur = conn.cursor()
    sql_query = """CREATE TABLE books(
        id interger PRIMARY KEY,
        author text NOT NULL ,
        title text NOT NULL 

    )"""

    cur.execute(sql_query)

def dbconnetion(): 
    conn = None 
    try :
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.Error as e:
        print(e)
    return conn
    