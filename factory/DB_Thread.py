#DB관련 스레드 클래스
import threading
import pymysql
import datetime

class DBconn(threading.Thread):
    def __init__(self, threadmanager):
        #스레드 초기화
        threading.Thread.__init__(self)
        #관리할 클래스 저장
        self.tm=threadmanager
        self.count=0
        #DB 연결 관련 설정
        #DB 연결
        self.conn = pymysql.connect( host='localhost', user='root', password='1234', charset='utf8', db='factory')
        #DB 작업을 위한 cursor 열기, dictionary형태로 호출
        self.cursor=self.conn.cursor(pymysql.cursors.DictCursor)
        #현재 제원의 기본키 저장을 위한 변수
        self.no=0
        #공정 날짜 저장
        self.today=datetime.datetime.now().strftime('%Y-%m-%d')
    
    #쓰레드 시작
    def run(self):
        while True:
            #현재 DB에서 재원의 컬럼이 변하는 지 확인
            if self.count<self.check_setValue():
                #컬럼이 변할시, 학습 또는 사용자에 의해 제어된 값이 추가 된것으로 간주
                #값을 다시 불러오기
                self.get_SetValue()
            
    #DB에서 최근의 제원값 가져오기
    def get_SetValue(self):
        #가져온후 tm에 전달
        self.cursor.execute("select * from setting_value limit 1")
        rows=self.cursor.fetchall()
        for i in rows:
            self.no=i['no']
            #가져온 데이터중 무게, 열리는 시간, 오차 범위 불러옴
            return i['target_weight'], i['open_time'], i['target_range'],

    #측정 데이터 저장 무게와 판별 결과 저장
    def input_Value(self, weight, value):
        sql="insert into product(weight,date,result,set_value) values(%s,%s,%s,%s)"
        self.cursor.execute(sql,(weight,self.today,value,self.no))
        self.conn.commit()
    #DB의 변화 확인,
    #학습 또는 사용자가 데이터의 수정으로 이러나는 컬럼 추가 확인
    def check_setValue(self):
        pass
