import threading
import Threadmain
import socket
import time

##각 모듈과 연결되는 쓰레드 클래스->쓰레드 상속 받아옴
class Client(threading.Thread):
    ##생성시 소캣정보(client), 주소(ip주소, port, 쓰래드 관리 클래스를 받아온다.)
    def __init__(self,index,client,mainThread):
        threading.Thread.__init__(self)
        self.index=index
        self.tm=mainThread
        self.client=client

    def do_job(self):
        pass 
    
    ##쓰레드 실행
    def run(self):
        #현재 전체공정이 진행중이라면 재접속한 client에서 자동 시작 요청
        if self.tm.main_state=='start':
            self.send_to_device("start")
        ##계속적인 수신
        try:
            self.do_job()
        except Exception as err:
            print(err)
            print(self.tm.thread_dic)
            self.tm.remove_client(self)
            self.client.close()
            print(self.name+"client finish")

    ##내가 받은 내용 같은 관리 클래스에 들어있는 쓰레드에게 전송
    ##원하는 이름의 공저으로 전송 가능(to_Client에 원하는 공정이름 지정시))
    def send_to_thread(self,to_Client,message):
        self.tm.thread_dic[to_Client].send_to_device(message)

    ##자신의 공정에게 메시지 전달
    def send_to_device(self,message):
        print(self.index,message)
        self.client.send(message.encode())