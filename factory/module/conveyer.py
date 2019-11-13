from module.Thread_client import Client
from module.factory_enum import device
class Conveyer(Client):
    def __init__(self,index, client, mainThread):
        Client.__init__(self,index,client,mainThread)

    def do_job(self):
        while True:
                self.content=self.client.recv(32)
                message=str(self.content)[1:].strip("'")
                temp=message.split(";")
                print(temp)
                if temp[0]=="B":
                    print("B stop")
                    self.send_to_thread(device.PRODUCT_DISPENSOR, temp[1]+'\n')
                elif temp[0]=="C":
                    print("C stop")
                    self.send_to_thread(device.WEIGHT_SENSOR, temp[1]+'\n')
               