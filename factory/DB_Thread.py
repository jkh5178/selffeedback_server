import threading
class DBconn(threading.Thread):
    def __init__(self, threadmanager):
        threading.Thread.__init__(self)
        self.tm=threadmanager
        self.count=1
        #DB 연결 관련 설정

    def run(self):
        while True:
            if count<self.check_setValue():
                self.get_SetValue()
            

    def get_SetValue(self):
        #DB에서 제원값 가져오기
        #가져온후 tm에 전달
        pass
    
    def input_Value(self, weight, value):
        #DB에 판별값 및 값 저장
        pass

    def check_setValue(self):
        pass
