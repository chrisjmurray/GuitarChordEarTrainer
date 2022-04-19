import sqlite3
from sqlite3 import Error
import re
import os
import random

dirpath = os.path.dirname(__file__)
dbpath = os.path.join(dirpath, 'Data', 'data.db')
csvpath = os.path.join(dirpath,'Data','voicings.csv')

sql_create_voicings_table = """ CREATE TABLE IF NOT EXISTS fingerings (
                                    fingering text NOT NULL PRIMARY KEY,
                                    tag text
                                    ); """

def create_connection():
    try:
        conn = sqlite3.connect(dbpath)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def drop_table(conn):
    drop_sql = """DROP TABLE fingerings;"""
    try:
        conn.execute(drop_sql)
    except Error as e:
        print(e)

def insert_fingering(conn, fingering):
    sql = '''INSERT INTO fingerings(fingering, tag)
             VALUES(?,?)''' 
    cur = conn.cursor()
    try:
        cur.execute(sql, fingering)
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(fingering)

def readin_csv(conn, filepath=csvpath):
    with open(filepath) as f:
        tag = 'NULL'
        for line in f:
            if re.match(r'^#.+,,,,,$', line):
                tag = line[1:-6]
                continue
            if re.match(r"^((-1|[0-4]),){5}(-1|[0-4])$", line):
                fingering = line[:-1]
                x = insert_fingering(conn, (fingering, tag))
            

def refresh_db():
    conn = create_connection()
    drop_table(conn)
    create_table(conn, sql_create_voicings_table)
    readin_csv(conn)
    conn.close()



select_rand_sql1 = """SELECT * FROM fingerings where tag='"""
select_rand_sql2 = """' ORDER BY RANDOM() LIMIT 1; """

def fetchrandfing():
    conn = create_connection()
    c = conn.cursor()
    #get list of distinct tags
    c.execute("""select distinct tag from fingerings;""")
    tags = c.fetchall()
    #pick random tag, the [0] grabs the string from the tuple
    tag = random.choice(tags)[0]
    c.execute(select_rand_sql1+tag+select_rand_sql2)
    record = c.fetchall()
    conn.close()
    return record[0] #index to grab the single tuple from the list

print(fetchrandfing())