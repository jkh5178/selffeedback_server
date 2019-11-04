import threading
import Threadmain
import socket

##각 모듈과 연결되는 쓰레드 클래스->쓰레드 상속 받아옴
class Client(threading.Thread):
    ##생성시 소캣정보(client), 주소(ip주소, port, 쓰래드 관리 클래스를 받아온다.)
    def __init__(self,client,addr,mainThread):
        threading.Thread.__init__(self)
        self.tm=mainThread
        self.client=client
        self.addr=addr
    ##쓰레드 실행
    def run(self):
        ##쓰레드 실행하면서 공정에서 보내는 공정 이름 받기
        self.content = self.client.recv(32)
        ##공정 이름 저장
        self.name = str(self.content)[1:].strip("'")
        ##공정 구분 분기점
        print(self.name)
        if self.name=='B':
            self.send_to='D'##원하는 쓰래스의 공정이름 저장
        elif self.name=='D':
            self.send_to='B'
        ##계속적인 수신
        try:
            while True:
                self.content=self.client.recv(32)
                message=str(self.content)[1:].strip("'")
                print(message)
                self.broadcast(self.send_to,message+'\n')
        except Exception as err:
            print(err)
            print(self.tm.thread_list)
            self.tm.remove_client(self)
            self.client.close()
            print("client finish")

    ##자신의 이름 다른 클래스에게 알려주기
    def getName(self):
        return self.name
    ##내가 받은 내용 같은 관리 클래스에 들어있는 쓰레드에게 전송
    ##원하는 이름의 공저으로 전송 가능(to_Client에 원하는 공정이름 지정시))
    def broadcast(self,to_Client,message):
        for temp in self.tm.thread_list:
            if temp.getName()==to_Client:
                temp.send(message)
    ##자신의 공정에게 메시지 전달
    def send(self,message):
        self.client.send(message.encode())