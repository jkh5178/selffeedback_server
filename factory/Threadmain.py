import  module.Thread_client
import  DB_Thread
from  module.product_dispensor import ProductDipensor
from  module.weight_sensor import WeightSeneor
from  module.conveyer import Conveyer
from  module.cup_dispensor import CupDispensor
from  module.factory_enum import device
from module.master import Master
from module.remain_sensor import RemainSensor
import time
##쓰래드를 관리하는 클래스
class Threadmain:
    ##클래스 생성시 쓰레드를 담을 list 생성
    def __init__(self):
        #DB연결 부분
        self.db= DB_Thread.DBconn(self)
        #DB에 연결하여 가져올 데이터
        #목표량, 물건을 넣을 시간, 오차 범위 가져오기
        self.target_weight,self.opentime, self.target_range=self.db.get_SetValue()
        print(self.target_weight,self.opentime, self.target_range)

        self.count=0#생산량

        #스레드의 관리를 위한 list
        self.thread_dic={}

        #현제 전체 공정 상태 관리
        self.main_state="end"
    
    ##쓰레드 만들기(소캣(클라이언트)과 주소를 받아옴)
    def make_thread(self, socket, addr):
        ##쓰래드 클라이언트 생성
        ##소캣 정보와 주소와 자기자
        content=socket.recv(32)
        message=str(content)[1:].strip("'")
        print(self.thread_dic)
        if message == "A":
            cd = CupDispensor(index=device.CUP_DISPENSOR,client=socket,mainThread=self)
            self.thread_dic[cd.index] = cd
            cd.start()
        elif message == "B":
            pd = ProductDipensor(index=device.PRODUCT_DISPENSOR,client=socket,mainThread=self,opentime=self.opentime)
            self.thread_dic[pd.index] = pd
            pd.start()
        elif message == "C":
            ws = WeightSeneor(index=device.WEIGHT_SENSOR,client=socket,mainThread=self,target_range= self.target_range, target_weight=self.target_weight)
            self.thread_dic[ws.index] = ws
            ws.start()
        elif message == "D":
            convey = Conveyer(index=device.CONVEYER,client=socket,mainThread=self)
            self.thread_dic[convey.index] = convey
            convey.start()
        elif message =="E":
            remain_sensor=RemainSensor(index=device.REMAINSENSOR, client=socket, mainThread=self)
            self.thread_dic[remain_sensor.index] = remain_sensor
            remain_sensor.start()
        elif message == "master":
            master = Master(index=device.MASTER, client=socket, mainThread=self)
            self.thread_dic[master.index] = master
            master.start()
    #소캣 list에서 삭제
    def remove_client(self,thread):
        print(thread)
        del(self.thread_dic[thread.index])
        #소캣 전체 시작
    def start(self):
        print("start")
        self.main_state="start"
        for temp in self.thread_dic:
            print(self.thread_dic[temp])
            self.thread_dic[temp].send_to_device(self.main_state)
    
    #소캣 전체 정지
    def stop(self):
        print("end")
        self.main_state="end"
        self.thread_dic[device.CUP_DISPENSOR].client.close()
        self.thread_dic[device.PRODUCT_DISPENSOR].client.close()
        self.thread_dic[device.WEIGHT_SENSOR].client.close()
        self.thread_dic[device.CONVEYER].client.close()
    #C에서 전송한 데이터 DB로 저장
    def savedata(self,weight, value):
        self.db.input_Value(weight, value)
    

    def refrash_data(self):
        self.target_weight,self.opentime, self.target_range=self.db.get_SetValue()
        self.stop()
        time.sleep(30)
        if len(self.thread_dic)==5:
            self.start()
    def lean_thread(self):
        self.db.startTread()