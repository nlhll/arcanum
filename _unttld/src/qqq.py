import os
import pandas
import sqlite3


table_name = 'ISO_TC 213'
csv_conn = pandas.read_csv('..\\dataset\\ISO_TC 213.csv')
conn = sqlite3.connect('..\\database\\db.db')
csv_conn.to_sql(table_name, conn, if_exists='append', index=False)
# print(os.path.dirname(os.path.abspath(__file__)))