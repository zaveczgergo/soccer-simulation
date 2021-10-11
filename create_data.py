#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd

con = sqlite3.connect("temp/cfo-data-analysis.db")
cur = con.cursor()

try:
    cur.execute("ALTER TABLE 'kaggle-events' RENAME TO kaggle_events;")
    cur.fetchall()
except:
    pass

#https://stackoverflow.com/questions/305378/list-of-tables-db-schema-dump-etc-using-the-python-sqlite3-api/33100538#33100538
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

for table_name in tables:
    table = pd.read_sql("""SELECT * FROM {};""".format(table_name[0]), con)
    table.to_csv("temp/" + table_name[0] + "-part.csv", index_label="index")
    
con.close()