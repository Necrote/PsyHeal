#!/usr/bin/python

import sqlite3 as sql
dbPath = "src/database/"
error = None

try:
    usr = "rootadmin"
    pwd = "asdf@123"
    accType = "admin"

    conn = sql.connect(dbPath+"psyheal.db")
    conn.execute("CREATE TABLE IF NOT EXISTS user(username text PRIMARY KEY, password text NOT NULL, accType text NOT NULL, CONSTRAINT chkAccType CHECK(accType IN ('admin', 'doctor', 'patient')) )")
    conn.commit()

    cur = conn.cursor()
    cur.execute("INSERT INTO user(username,password,accType) VALUES (?,?,?)",(usr,pwd,accType))
    conn.commit()

except:
    conn.rollback()
    error = "Some error occured while setup procedure!"

finally:
    conn.close()
    if error:
        print (error)
    else:
        print ('''****************************************************
        Setup done!\n****************************************************
        Inital admin credentials-
        username: ''' + usr + '''
        password: ''' + pwd)