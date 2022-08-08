#!/usr/bin/python

import sqlite3
import os
DB_FILENAME = "test.db"

def init(wipeData=False):
    conn = sqlite3.connect(DB_FILENAME)
    print("Opened database successfully")


    # Create tables
    conn.execute('''CREATE TABLE IF NOT EXISTS categories
                (cId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                name TEXT
                )''')
                
    conn.execute('''CREATE TABLE IF NOT EXISTS teams
                (tId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                name TEXT, 
                description TEXT,
                cId INTEGER,
                pwd TEXT,
                year INTEGER,
                FOREIGN KEY (cId) REFERENCES categories(cId)
                )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS matches
                (mId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                cId INTEGER NOT NULL,
                homeId INTEGER NOT NULL,
                guestId INTEGER NOT NULL,
                homeScore INTEGER,
                guestScore INTEGER,
                winnerId INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (mId) REFERENCES matches(mId),
                FOREIGN KEY (cId) REFERENCES categories(cId),
                FOREIGN KEY (homeId) REFERENCES teams(tId),
                FOREIGN KEY (guestId) REFERENCES teams(tId),
                FOREIGN KEY (winnerId) REFERENCES teams(tId)
                )''')


    print("Tables created successfully")

    conn.close()


def purge(hard=False):
    
    if hard:
        if os.path.isfile(DB_FILENAME):
            os.remove(DB_FILENAME)
            print("DB File removed.")
        else:
            print("DB File not found.")
    else:
        conn = sqlite3.connect(DB_FILENAME)
        conn.execute('''DROP TABLE IF EXISTS teams''') 
        conn.execute('''DROP TABLE IF EXISTS categories''')
        conn.execute('''DROP TABLE IF EXISTS matches''')
        print("Tables dropped successfully")
        conn.close()

if __name__ == "__main__":
    purge(hard=True)
    init()


