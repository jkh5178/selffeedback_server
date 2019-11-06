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
            #self.client.send(self.tm.timetoopen)#초기화 시 현재 DB의 열리는 시간 값 전송
            self.send_to='D'##원하는 쓰래스의 공정이름 저장
        elif self.name=='D':
            self.send_to='B'
        elif self.name=='C':
            self.target=self.tm.target_weight
        ##계속적인 수신
        try:
            while True:
                self.content=self.client.recv(32)
                message=str(self.content)[1:].strip("'")
                ##C,B공정에서 정수를 전송하는 경우 추가
                print(message)
                if self.name=='master':
                    if message=='s':
                        self.tm.start()
                    elif message=='e':
                        self.tm.stop()
                elif(self.name=='B' or self.name=='D'):
                    self.broadcast(self.send_to,message+'\n')
                elif(self.name=='C'):
                    self.weight=int(message)
                    if(self.weight>=self.target*0.08 and self.weight<=self.target*1.02):
                        self.send("true\n")
                        self.tm.savedata(self.weight,"true")
                    else:
                        self.send("false\n")
                        self.tm.savedata(self.weight,"false")
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