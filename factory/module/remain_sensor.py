from module.Thread_client import Client
from module.factory_enum import device
class RemainSensor(Client):
    def __init__(self,index, client, mainThread):
        Client.__init__(self,index,client,mainThread)
    def do_job(self):
        while True:
            self.content=self.client.recv(32)
            message=str(self.content)[1:].strip("'")
            print(message)
            self.send_to_thread(device.MASTER,"remain;"+message)