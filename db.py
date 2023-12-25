import sqlite3

conn = sqlite3.connect('database.db')

def create_new_file(header:str, filepath:str, token:str):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO files (header, path_to_file) VALUES (?, ?) RETURNING id_file", (header, filepath))
    id = c.fetchone()
    c.execute("INSERT INTO notes (token, id_file) VALUES (?, ?)", (token, id[0]))
    conn.commit()
    conn.close()
    
def get_files(token:str):
    files = []
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id_file FROM notes WHERE token=(?)", (token,))
    ids = c.fetchall()
    for id in ids:
        id_value = id[0]
        c.execute("SELECT header, path_to_file FROM files WHERE id_file = (?)", (id_value,))
        data = c.fetchone()
        files.append(data)
    conn.commit()
    conn.close()
    return files

def check_token(token: str) -> bool:
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id_file FROM notes WHERE token=(?)", (token,))
    d = c.fetchone()
    return d is not None and len(d) > 0 


c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        token TEXT NOT NULL,
        id_file INTEGER);
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS files(   
        id_file INTEGER PRIMARY KEY AUTOINCREMENT,
        header TEXT,
        path_to_file TEXT NOT NULL);
""")

conn.commit()
conn.close()

#print(check_token("youfucked_down"))
#create_new_file("fuck you", "/etc/fuckyou", "youfucked_down")
#print(get_files("youfucked_down"))
#create_new_file("love you", "/etc/loveyou", "you")
#print(get_files("you"))
