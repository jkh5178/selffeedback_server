import Thread_client
import DB_Thread
##쓰래드를 관리하는 클래스
class Threadmain:
    ##클래스 생성시 쓰레드를 담을 list 생성
    def __init__(self):
        #DB연결 부분
        self.db=DB_Thread.DBconn(self)
        self.db.get_SetValue()

        self.count=0
        self.thread_list=[]
        #DB에 연결하여 가져올 데이터
        #목표량, 물건을 넣을 시간,현재 공정의 상태
        self.target_weight=20
        self.opentime=2000
        self.main_state="end"
    
    ##쓰레드 만들기(소캣(클라이언트)과 주소를 받아옴)
    def make_thread(self, socket, addr):
        ##쓰래드 클라이언트 생성
        ##소캣 정보와 주소와 자기자신을 기억 시킨다.
        print(self.thread_list)
        client=Thread_client.Client(socket,addr,self)
        ##생성된 쓰레드 객체를 list에 추가한다.
        self.thread_list.append(client)
        ##쓰래드를 실행한다.
        client.start()
    def remove_client(self,socket):
        print(socket)
        self.thread_list.remove(socket)

    def start(self):
        print("start")
        self.main_state="start"
        for temp in self.thread_list:
            temp.send("start")
    def stop(self):
        print("end")
        self.main_state="end"
        for temp in self.thread_list:
            name=temp.getName()
            print("end module"+name)
            if(name=="D"):
                temp.client.close()
                continue
            if(name=="A"):
                temp.client.close()
                continue
            if(name=="C"):
                temp.client.close()
                continue
            temp.send("end")


    def savedata(self,weight, value):
        self.db.input_Value(weight, value)
