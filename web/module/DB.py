import pymysql
import pandas as pd
class Db():
    def __init__(self):
        self.conn = pymysql.connect( host='localhost', user='root', password='1234', charset='utf8', db='factory')
        self.cursor=conn.cursor(pymysql.cursors.DictCursor)
    
    def read_data_dataframe(self,qurey):
        return pd.read_sql_query(qurey,self.conn)
        
    def input_data(self,qurey):
        self.cursor.execute(qurey)
        self.conn.commit()
