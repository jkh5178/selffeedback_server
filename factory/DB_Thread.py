#DB관련 스레드 클래스
import threading
import pymysql
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import time

class DBconn():
    def __init__(self, threadmanager):
        #스레드 초기화
        
        #관리할 클래스 저장
        self.tm=threadmanager
        self.count=0
        #DB 연결 관련 설정
        #DB 연결
        self.conn = pymysql.connect( host='localhost', user='root', password='1234', charset='utf8', db='factory')
        #DB 작업을 위한 cursor 열기, dictionary형태로 호출
        self.cursor=self.conn.cursor(pymysql.cursors.DictCursor)
        #현재 제원의 기본키 저장을 위한 변수
        self.setting_no=0
        self.product_no=0
        #공정 날짜 저장
        self.today=datetime.datetime.now().strftime('%Y-%m-%d')
        
    
    def startTread(self):
        self.leaning_tread=threading.Thread(target=self.run())
        self.leaning_tread.start()
    #쓰레드 시작
    def run(self):
        #현재 DB에서 재원의 컬럼이 변하는 지 확인
            self.update_set_value( self.lean_data())
            self.tm.refrash_data()
            self.stoptTread()

    def stoptTread(self):
        self.leaning_tread.join()

    def get_product_value(self, product):
        self.cursor.execute("select * from product where %s limit 1",(product))
        rows=self.cursor.fetchall()
        for i in rows:
            self.product_no=i['no']
    #DB에서 최근의 제원값 가져오기
    def get_SetValue(self):
        #가져온후 tm에 전달
        self.cursor.execute("select * from setting_value ORDER BY no DESC limit 1")
        rows=self.cursor.fetchall()
        print(rows)
        for i in rows:
            self.setting_no=i['no']
            #가져온 데이터중 무게, 열리는 시간, 오차 범위 불러옴
            return i['target_weight'], i['open_time'], i['target_range']

    #측정 데이터 저장 무게와 판별 결과 저장
    def input_Value(self, weight, value):
        sql="insert into log(date,weight,result,settingnum,productnum) values(%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,(self.today,weight,value,self.setting_no,self.product_no))
        self.conn.commit()
    #DB의 변화 확인,
    #학습 또는 사용자가 데이터의 수정으로 이러나는 컬럼 추가 확인
    def update_set_value(self,opentime):
        sql="insert into setting_value(open_time,target_weight,target_range) values(%s,%s,%s)"
        self.cursor.execute(sql,(str(opentime), self.tm.target_weight, self.tm.target_range))
        self.conn.commit()

    def lean_data(self):
        sql="select log.date,log.weight,log.result, setting_value.open_time, setting_value.target_weight from log, setting_value where log.settingnum=setting_value.no"
        data = pd.read_sql_query(sql,self.conn)
        x=pd.DataFrame(data['weight'])
        y=pd.DataFrame(data['open_time'])
        model=LinearRegression()
        model.fit(x,y)
        print(model.coef_, model.intercept_)
        new_time=model.predict([[self.tm.target_weight]])
        return new_time[0][0]