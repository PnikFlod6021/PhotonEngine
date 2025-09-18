import sqlite3

# define connector
def connect_data():
    return sqlite3.connect('../../photon.db')

# define cursor
def init_db():
    con = connect_data()
    cursor = con.cursor()

    # create table
    command = """CREATE TABLE IF NOT EXISTS players(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, score INTEGER DEFAULT 0) """

    cursor.execute(command)

    con.commit()
    con.close()

def list_players():
        con = connect_data()
        cursor = con.cursor()
        cursor.execute("SELECT id, name, score FROM players")
        rows = cursor.fetchall()
        con.close()
        return rows

def clear_players():
     con = connect_data()
     cursor = con.cursor()
     cursor.execute("DELETE FROM players")
     con.commit()
     con.close()

def search():
     con = connect_data()
     cursor = con.cursor()
     cursor.execute("SELECT id FROM players WHERE id = ?")
     con.commit()
     con.close()





