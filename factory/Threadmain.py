import Thread_client
import DB_Thread
##쓰래드를 관리하는 클래스
class Threadmain:
    ##클래스 생성시 쓰레드를 담을 list 생성
    def __init__(self):
        #DB연결 부분
        self.db=DB_Thread.DBconn(self)
        #DB에 연결하여 가져올 데이터
        #목표량, 물건을 넣을 시간, 오차 범위 가져오기
        self.target_weight,self.opentime, self.target_range=self.db.get_SetValue()
        print(self.target_weight,self.opentime, self.target_range)
        self.count=0
        #스레드의 관리를 위한 list
        self.thread_list=[]
        #현제 전체 공정 상태 관리
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
    #소캣 list에서 삭제
    def remove_client(self,socket):
        print(socket)
        self.thread_list.remove(socket)
    #소캣 전체 시작
    def start(self):
        print("start")
        self.main_state="start"
        for temp in self.thread_list:
            temp.send("start")
    
    #소캣 전체 정지
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
    #C에서 전송한 데이터 DB로 저장
    def savedata(self,weight, value):
        self.db.input_Value(weight, value)
