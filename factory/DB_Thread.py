import threading
import pymysql
import datetime
class DBconn(threading.Thread):
    def __init__(self, threadmanager):
        threading.Thread.__init__(self)
        self.tm=threadmanager
        self.count=1
        #DB 연결 관련 설정
        self.conn = pymysql.connect( host='localhost', user='root', password='1234', charset='utf8', db='factory')
        self.cursor=self.conn.cursor(pymysql.cursors.DictCursor)
        self.no=0
        self.today=datetime.datetime.now().strftime('%Y-%m-%d')
    def run(self):
        while True:
            if count<self.check_setValue():
                self.get_SetValue()
            

    def get_SetValue(self):
        #DB에서 제원값 가져오기
        #가져온후 tm에 전달
        self.cursor.execute("select * from setting_value limit 1")
        rows=self.cursor.fetchall()
        for i in rows:
            self.no=i['no']
            return i['target_weight'], i['open_time'], i['target_range'],

    
    def input_Value(self, weight, value):
        #DB에 판별값 및 값 저장
        sql="insert into product(weight,date,result,set_value) values(%s,%s,%s,%s)"
        self.cursor.execute(sql,(weight,self.today,value,self.no))
        self.conn.commit()
    def check_setValue(self):
        pass
