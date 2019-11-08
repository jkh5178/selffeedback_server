import threading
import Threadmain
import socket
import time
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
            print(str(self.tm.opentime))
            self.send(str(self.tm.opentime))#초기화 시 현재 DB의 열리는 시간 값 전송
            self.send_to='D'##원하는 쓰래스의 공정이름 저장
        elif self.name=='C':
            print(self.tm.target_weight)
            self.send(str(self.tm.target_weight)+'\n')
            self.send(str(self.tm.target_range)+'\n')

        #현재 전체공정이 진행중이라면 재접속한 client에서 자동 시작 요청
        if self.tm.main_state=='start':
            self.send("start")
        
        ##계속적인 수신
        try:
            while True:
                self.content=self.client.recv(32)
                message=str(self.content)[1:].strip("'")
                print(message)
                ##각 공정별 수행 작업 분류
                if self.name=='master':#master : 전체 공정의 시작과 끝 제어
                    if message=='s':
                        self.tm.start()
                    elif message=='e':
                        self.tm.stop()
                #D 공정 B,C공정에 각각 센서의 정보를 통해 값을 전달(컨베이어가 멈추었다는 정보)
                #해당 메세지를 받을 경우 B,C공정에서 각각 작업 수행 시작
                elif (self.name=='D'):
                    temp=message.split(";")
                    print(temp)
                    if temp[0]=="B":
                        print("B stop")
                        self.broadcast(temp[0],temp[1]+'\n')
                    elif temp[0]=="C":
                        print("C stop")
                        self.broadcast(temp[0],temp[1]+'\n')
                #B공정 연결시 미리 세팅된 D에게 메세지를 보넨다.
                elif(self.name=='B'):
                    self.broadcast(self.send_to,message+'\n')
                #C공정 
                elif(self.name=='C'):
                    #C에서 go2라는 메시지가 서버로 올시 D에게 메시지 전달
                    if message=="go2":
                        self.broadcast("D",message+'\n')
                    #그외에는 무게 측정 값이 전달 됨으로 판별후 DB에 저장
                    else:
                        self.weight=float(message)
                        if(self.weight>=self.tm.target_weight-self.tm.target_weight*0.02 and self.weight<=self.tm.target_weight+self.tm.target_weight*0.02):
                            print(self.weight,"ture")
                            self.tm.savedata(self.weight,1)
                        else:
                            print(self.weight,"flase")
                            self.tm.savedata(self.weight,0)
        #연결이 갑작스럽게 종료 될 경우
        #연결을 해제한다
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