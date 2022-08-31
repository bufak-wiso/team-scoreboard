#!/usr/bin/python

import sqlite3
import os
import pandas as pd
DB_FILENAME = "test.db"

def init(conn, testdata=False, wipeData=False):
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
                year TEXT,
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
    if testdata: fill_testdata(conn)


def purge(conn, hard=False):
    
    if hard:
        if os.path.isfile(DB_FILENAME):
            os.remove(DB_FILENAME)
            print("DB File removed.")
        else:
            print("DB File not found.")
    else:
        conn.execute('''DROP TABLE IF EXISTS teams''') 
        conn.execute('''DROP TABLE IF EXISTS categories''')
        conn.execute('''DROP TABLE IF EXISTS matches''')
        print("Tables dropped successfully")
        

def fill_testdata(conn):
    # insert into categories
    # conn.execute('''INSERT INTO categories (cId, name)
    #                 VALUES (NULL, "Test Category")''')

    c_data=pd.DataFrame({"cId": [None, None], "name": ["Flunkyball", "Beerpong"]})
    c_data.to_sql('categories', con = conn, if_exists = 'append', index=False)

    t_data=pd.DataFrame({"tId": [None, None, None, None, None], "name": ["FC Suffenhausen", "1.FC Partyborn", "Bufak Allstars", "Pong zur Bong", "Die fanstastischen Vier"], "description": ["Nur der BVB!", "Partyborn, Junge!", "Wir wissen, wo es läuft!", "420", "Wir bleiben TROY"], "cId": [1,1,2,2,1], "pwd": ["111", "222", "333", "444", "555"], "year": ["2022", "2022", "2022", "2022", "2022"]})
    t_data.to_sql('teams', con = conn, if_exists = 'append', index=False)

    m_data=pd.DataFrame({"mId": [None, None, None, None, None], "cId": [1,2,1,1,1], "homeId": [1,3,2,2,5], "guestId": [2,4,1,1,2], "homeScore": [0,0,1,0,1], "guestScore": [1,1,0,1,0], "winnerId": [2,4,2,1,5]})
    m_data.to_sql('matches', con = conn, if_exists = 'append', index=False)

if __name__ == "__main__":
    conn = sqlite3.connect(DB_FILENAME)
    purge(conn, hard=True)
    init(conn, testdata=False)
    conn.close()


