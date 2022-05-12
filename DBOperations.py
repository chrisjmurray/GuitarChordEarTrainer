import sqlite3
from sqlite3 import Error
import re
import os
import random

dirpath = os.path.dirname(__file__)
dbpath = os.path.join(dirpath, 'Data', 'data.db')
csvpath = os.path.join(dirpath,'Data','voicings.csv')

sql_create_fingerings_table = """ CREATE TABLE IF NOT EXISTS fingerings (
                                    fingering text NOT NULL PRIMARY KEY
                                    ); """

sql_create_tags_table = """ CREATE TABLE IF NOT EXISTS tags (
                                    tag_title text NOT NULL UNIQUE,
                                    tag_id INTEGER PRIMARY KEY
                                    ); """

sql_create_fingerings_tags_table = """ CREATE TABLE IF NOT EXISTS fingerings_tags (
                                    fingering text NOT NULL,
                                    tag_id INTEGER 
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
    drop_sql_tags = """DROP TABLE tags;"""
    drop_sql_tags_fingerings = """DROP table tags_fingerings"""
    try:
        conn.execute(drop_sql)
        conn.execute(drop_sql_tags)
        conn.execute(drop_sql_tags_fingerings)
    except Error as e:
        print(e)

def insert_fingering(conn, fingering, tags):
    sql_fingering = '''INSERT INTO fingerings(fingering)
                       VALUES(?)''' 
    sql_tags =  '''INSERT INTO tags(tag_title)
                   VALUES(?)''' 
    sql_tags_fingerings = '''INSERT INTO fingerings_tags(fingering, tag_id)
                             VALUES(?,?)'''
    sql_select_tag_id = '''SELECT tag_id FROM tags
                           WHERE tag_title = ? '''
    cur = conn.cursor()
    try:
        cur.execute(sql_fingering, (fingering,))
        for tag in tags:
            cur.execute(sql_select_tag_id, (tag,))
            tag_ids = cur.fetchall()
            if len(tag_ids) == 0:
                cur.execute(sql_tags, (tag,))
                cur.execute(sql_select_tag_id, (tag,))
                tag_ids = cur.fetchall()
                cur.execute(sql_tags_fingerings, (fingering, tag_ids[0][0],))
            else:
                cur.execute(sql_tags_fingerings, (fingering, tag_ids[0][0],))
                
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(fingering)

def readin_csv(conn, filepath=csvpath):
    with open(filepath) as f:
        tag = 'NULL'
        for line in f:
            if re.match(r'^#.+,,,,,$', line):
                tags = line[1:-6]
                continue
            if re.match(r"^((-1|[0-4]),){5}(-1|[0-4])$", line):
                fingering = line[:-1]
                x = insert_fingering(conn, fingering, [tags])
            

def refresh_db():
    conn = create_connection()
    drop_table(conn)
    create_table(conn, sql_create_fingerings_table)
    create_table(conn, sql_create_tags_table)
    create_table(conn, sql_create_fingerings_tags_table)
    readin_csv(conn)
    conn.close()



select_rand_sql1 = """SELECT * FROM fingerings_tags where tag_id="""
select_rand_sql2 = """ ORDER BY RANDOM() LIMIT 1; """

def fetchrandfing():
    conn = create_connection()
    c = conn.cursor()
    #get all tags
    #pick one of those tags
    #pick one fingering with that tag
    c.execute("""select distinct tag_id from tags;""")
    tag_ids = c.fetchall()
    #pick random tag, the [0] grabs the string from the tuple
    tag = random.choice(tag_ids)[0]
    c.execute(select_rand_sql1+str(tag)+select_rand_sql2)
    record = c.fetchall()
    conn.close()
    return record[0] #index to grab the single tuple from the list
