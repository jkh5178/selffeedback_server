'''
import pymysql
import pandas as pd

conn = pymysql.connect( host='192.168.0.2', user='jkh', password='1234', charset='utf8', db='factory')
cursor=conn.cursor(pymysql.cursors.DictCursor)

#cursor.execute("select * from log")#sql문 실행
#data=cursor.fetchall()#select문에서만
#conn.commit() #insert, delete명령시 사용
data=pd.read_sql_query('select * from log',conn)
print(data)
'''
from module.DB import Db

db=Db()
print(db.read_data_dataframe("select * from log"))
