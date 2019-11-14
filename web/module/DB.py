import pymysql
import pandas as pd
class Db():
    def __init__(self):
        self.conn = pymysql.connect( host='192.168.0.2', user='jkh', password='1234', charset='utf8', db='factory')
        self.cursor=self.conn.cursor(pymysql.cursors.DictCursor)
    
    def read_data_dataframe(self,qurey):
        return pd.read_sql_query(qurey,self.conn)
        
    def input_data(self,qurey):
        self.cursor.execute(qurey)
        self.conn.commit()
