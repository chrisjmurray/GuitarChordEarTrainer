import sqlite3
from sqlite3 import Error
import re
import os
import random

dirpath = os.path.dirname(__file__)
dbpath = os.path.join(dirpath, 'Data', 'data.db')
csvpath = os.path.join(dirpath,'Data','voicings.csv')

# In the current structure, 3 tables are not necessary. However, I decided to create this structure 
# of tables so that, should I decide to add more content associated with fingerings, the program would 
# be extensible without modification to the existing logic

sql_create_fingerings_table = """ CREATE TABLE IF NOT EXISTS fingerings (
                                    fingering text NOT NULL PRIMARY KEY
                                    ); """

sql_create_tags_table = """ CREATE TABLE IF NOT EXISTS tags (
                                    tag_title text UNIQUE NOT NULL,
                                    tag_id INTEGER PRIMARY KEY,
                                    UNIQUE(tag_title, tag_id)
                                    ); """

sql_create_fingerings_tags_table = """ CREATE TABLE IF NOT EXISTS fingerings_tags (
                                    fingering text NOT NULL,
                                    tag_id INTEGER,
                                    UNIQUE(fingering, tag_id) 
                                    ); """

select_rand_sql1 = """SELECT * FROM fingerings_tags where tag_id="""
select_rand_sql2 = """ ORDER BY RANDOM() LIMIT 1; """

def create_connection():
    try:
        conn = sqlite3.connect(dbpath)
    except Error as e:
        print(e)

    return conn

def get_all_tags():
    '''returns all tags as a list of strings'''
    sql_select_alltagtitles = "select distinct tag_title from tags;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(sql_select_alltagtitles)
    tuples = cur.fetchall()
    tagtitles = []
    for tup in tuples:
        tagtitles.append(tup[0])
    conn.close()
    return tagtitles

def tags_list_to_string(tags):
    '''parameter tags is a list of tags in string format
    creates a string appropriate to use in sqlite statements
    e.g. select * from table where title in (tag1, tag2, tag3). 
    the returned string is everything in and including the parenthesis'''
    s = "("
    for tag in tags:
        s += "'"+tag+"'"+","
    s = s[:-1] #remove extra comma from the for loop
    s += ")"
    return s

def fetch_rand_fingering_from_tags(tags):
    ''':param List tags: list of tags in string format to include in the search.
    returns'''
    conn = create_connection()
    cur = conn.cursor()
    #select tag_id from tags where tag_title in given tags
    tagsliststring = tags_list_to_string(tags)
    cur.execute("select distinct tag_id from tags where tag_title in "+tagsliststring+";")  
    tag_ids = cur.fetchall() 
    #choose random tag
    tag_id = random.choice(tag_ids)[0]
    cur.execute(select_rand_sql1+str(tag_id)+select_rand_sql2)
    record = cur.fetchall()
    conn.close()
    return record[0]

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
    drop_sql_tags_fingerings = """DROP table fingerings_tags"""
    try:
        conn.execute(drop_sql)
        conn.execute(drop_sql_tags)
        conn.execute(drop_sql_tags_fingerings)
    except Error as e:
        print(e)

def insert_fingering(conn, fingering, tags):
    #conn = create_connection()
    sql_fingering = '''INSERT OR IGNORE INTO fingerings(fingering)
                       VALUES(?)''' 
    sql_tags =  '''INSERT OR IGNORE INTO tags(tag_title)
                   VALUES(?)''' 
    sql_tags_fingerings = '''INSERT OR IGNORE INTO fingerings_tags(fingering, tag_id)
                             VALUES(?,?)'''
    sql_select_tag_id = '''SELECT tag_id FROM tags
                           WHERE tag_title = ? '''
    cur = conn.cursor()
    try:
        #insert fingering
        #if no tags, tags=[untagged]
        #for tag in tags, insert tag, get tag_id, insert tag_id and fingering
        cur.execute(sql_fingering, (fingering,))
        if len(tags) == 0:
            tags = ['untagged']
        for tag in tags:
            cur.execute(sql_tags, (tag,))
            cur.execute(sql_select_tag_id, (tag,))
            tag_ids = cur.fetchall()
            cur.execute(sql_tags_fingerings, (fingering, tag_ids[0][0],))
        conn.commit()
        #conn.close()
        return cur.lastrowid
    except Error as e:
        conn.close()
        print(fingering)

def readin_csv(conn, filepath=csvpath):
    with open(csvpath) as f:
        for line in f:
            splitline = line.split(',')
            fingering = ','.join(splitline[:6])
            tags = []
            for item in splitline[6:]:
                if len(item) and item[0] == '#':
                    tags.append(item[1:].rstrip())
            x = insert_fingering(conn, fingering, tags)            

def refresh_db():
    conn = create_connection()
    drop_table(conn)
    create_table(conn, sql_create_fingerings_table)
    create_table(conn, sql_create_tags_table)
    create_table(conn, sql_create_fingerings_tags_table)
    readin_csv(conn)
    conn.close()

def fetchrandfing():
    '''returns a string representing a fingering'''
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
