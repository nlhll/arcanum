import os
import pandas
import sqlite3

DB_PATH = '../database'
FILE_PATH = 'D:/work/arcanum/_unttld/dataset//ISO_TC213.csv'

table_name = FILE_PATH.split('/')[-1].replace('.csv', '')
try:
    os.mkdir(DB_PATH)
except OSError:
    pass

conn = sqlite3.connect(DB_PATH + '//db.db')

df = pandas.read_csv(FILE_PATH)
df.to_sql(table_name, conn, if_exists='append', index=False)