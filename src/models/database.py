import psycopg2
from psycopg2 import sql


# connection parameters
connection_params = {
     'dbname' : 'photon',
     'user' : 'student',
}

# define connector
def connect_data():
    return psycopg2.connect(**connection_params)

# define cursor
# def init_db():
#     con = connect_data()
#     cursor = con.cursor()

#     # create table
#     command = """CREATE TABLE IF NOT EXISTS players(id INTEGER serial PRIMARY KEY, name TEXT NOT NULL) """

#     cursor.execute(command)
#     con.commit()
#     cursor.close()
#     con.close()

# add players
def add_player(codename):
     con = connect_data()
     cursor = con.cursor()
     cursor.execute("INSERT INTO players (name) VALUES (%s)",(codename, ))
     con.commit()
     con.close()

def list_players():
     con = connect_data()
     cursor = con.cursor()
     cursor.execute("SELECT * FROM players")
     rows = cursor.fetchall()
     cursor.close()
     con.close()
     return rows

def search(player_id):
     con = connect_data()
     cursor = con.cursor()
     cursor.execute("SELECT * FROM players WHERE id = %s", (player_id,))
     row = cursor.fetchone()
     cursor.close()
     con.close()
     return row





