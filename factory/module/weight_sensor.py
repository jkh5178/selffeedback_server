from module.Thread_client import Client
from module.factory_enum import device
class WeightSeneor(Client):
    
    def __init__(self,index,client,mainThread,target_weight,target_range):
        Client.__init__(self,index,client,mainThread)
        self.send_to_device(str(target_weight)+'\n')
        self.send_to_device(str(target_range)+'\n')
        self.target_weight=target_weight
        self.target_range=target_range*0.01
        self.result_message=""
    def do_job(self):
        while True:
                self.content=self.client.recv(32)
                message=str(self.content)[1:].strip("'")
                if message=="go":
                    self.send_to_thread(device.CONVEYER,message+'\n')
                    #그외에는 무게 측정 값이 전달 됨으로 판별후 DB에 저장
                    print(self.tm.count)
                    if(self.tm.count>4 and self.tm.count%2==0):
                        self.tm.lean_thread()

                    elif (self.tm.db.get_product_count()<=4):
                        self.tm.opentime-=200
                        self.tm.db.update_set_value(self.tm.opentime)
                        self.tm.refrash_data()
                    

                else:
                    self.weight=float(message)
                    if(self.check_weight(weight=self.weight)):
                        result_message="true"
                        print(self.weight,"ture")
                        self.tm.savedata(self.weight,1)
                    else:
                        result_message="false"
                        print(self.weight,"false")
                        self.tm.savedata(self.weight,0)
                    self.send_to_device(result_message)
                    self.tm.count+=1

    def check_weight(self, weight):
        if(weight>=self.target_weight-self.target_weight*self.target_range and weight<=self.target_weight+self.target_weight*self.target_range):
            return True
        else:
            return False