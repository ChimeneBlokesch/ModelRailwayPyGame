
import sqlite3
import os

conn = sqlite3.connect("treinen.db")

cursor = conn.cursor()
# cursor.execute("SELECT name FROM type;")
# print(f"Table Name : {cursor.fetchall()}")
cursor.execute("""CREATE TABLE IF NOT EXISTS plaatjes (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """)

# path = 'C:\\Users\\31683\\Documents\\Treinen\\Trein 26 dec 2021\\plaatjes'
for folder in ['plaatjes', 'treinen']:
    path = 'C:\\Users\\31683\\Documents\\Treinen\\Trein 26 dec 2021\\' + folder
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.png'):
                try:
                    cursor.execute(
                        """INSERT INTO plaatjes(name) VALUES(?)""", (f,))
                except sqlite3.IntegrityError:
                    continue
cursor.execute("""CREATE TABLE IF NOT EXISTS type (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL UNIQUE
                                    ); """)

for x in ["passagier", "goederen", "locomotief", "poppetje"]:
    try:
        cursor.execute("""INSERT INTO type(name) VALUES(?)""", (x,))
    except sqlite3.IntegrityError:
        ...

cursor.execute("""CREATE TABLE IF NOT EXISTS soort (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL UNIQUE,
                                        type_id int,
                                        FOREIGN KEY(type_id) REFERENCES type(id)
                                    ); """)

cursor.execute("""CREATE TABLE IF NOT EXISTS materialen (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        img int,
                                        trein int,
                                        FOREIGN KEY(img) REFERENCES plaatjes(id),
                                        FOREIGN KEY(trein) REFERENCES soort(id)
                                        UNIQUE(name, img, trein)
                                    ); """)

cursor.execute("SELECT name FROM plaatjes;")
print(f"Table Name : {cursor.fetchall()}")
conn.commit()
conn.close()
