import Thread_client
##쓰래드를 관리하는 클래스
class Threadmain:
    ##클래스 생성시 쓰레드를 담을 list 생성
    def __init__(self):
        self.count=0
        self.thread_list=[]
    
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
        for temp in self.thread_list:
            temp.send("start")
    def stop(self):
        for temp in self.thread_list:
            temp.send("stop")