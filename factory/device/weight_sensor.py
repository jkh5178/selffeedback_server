from device.Thread_client import Client
from device.factory_enum import device
class WeightSeneor(Client):
    def __init__(self,index,client,mainThread,target_weight,target_range):
        Client.__init__(self,index,client,mainThread)
        self.send_to_device(str(target_weight)+'\n')
        self.send_to_device(str(target_range)+'\n')
        self.target_weight=target_weight
        self.target_range=target_range*0.01
    def do_job(self):
        while True:
                self.content=self.client.recv(32)
                message=str(self.content)[1:].strip("'")
                if message=="go":
                    self.send_to_thread(device.CONVEYER,message+'\n')
                    #그외에는 무게 측정 값이 전달 됨으로 판별후 DB에 저장
                else:
                    self.weight=float(message)
                    if(self.check_weight(weight=self.weight)):
                        print(self.weight,"ture")
                        self.tm.savedata(self.weight,1)
                    else:
                        print(self.weight,"flase")
                        self.tm.savedata(self.weight,0)

    def check_weight(self, weight):
        if(weight>=self.target_weight-self.target_weight*self.target_range and weight<=self.target_weight+self.target_weight*self.target_range):
            return True
        else:
            return False