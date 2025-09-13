
import sqlite3
import os

from constants import CHARACTER_FOLDER

if __name__ == "__main__":
    conn = sqlite3.connect("trains.db")

    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS images (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL
                                        ); """)

    # Find the images
    for folder in ['images', 'trains', CHARACTER_FOLDER]:
        for root, dirs, files in os.walk(folder):
            for f in files:
                if not f.endswith('.png'):
                    continue

                try:
                    cursor.execute(
                        """INSERT INTO images(name) VALUES(?)""", (f,))
                except sqlite3.IntegrityError:
                    continue

    cursor.execute("""CREATE TABLE IF NOT EXISTS type (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL UNIQUE
                                        ); """)

    for x in ["passenger", "freight", "engine", "character"]:
        try:
            cursor.execute("""INSERT INTO type(name) VALUES(?)""", (x,))
        except sqlite3.IntegrityError:
            ...

    cursor.execute("""CREATE TABLE IF NOT EXISTS modelType (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL UNIQUE,
                                            type_id int,
                                            FOREIGN KEY(type_id) REFERENCES type(id)
                                        ); """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS materials (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            img int,
                                            trein int,
                                            FOREIGN KEY(img) REFERENCES images(id),
                                            FOREIGN KEY(trein) REFERENCES modelType(id)
                                            UNIQUE(name, img, trein)
                                        ); """)

    cursor.execute("SELECT name FROM images;")
    print(f"Table Name : {cursor.fetchall()}")
    conn.commit()
    conn.close()
