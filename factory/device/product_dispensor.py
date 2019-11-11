from Thread_client import Client
from factory_enum import device
class ProductDipensor(Client):
    def __init__(self,index,client,mainThread,opentime):
        Client.__init__(self,index=index,client=client,mainThread=mainThread)
        print(str(opentime))
        self.send_to_device(str(opentime))#초기화 시 현재 DB의 열리는 시간 값 전송
    def do_job(self):
        while True:
            self.content=self.client.recv(32)
            message=str(self.content)[1:].strip("'")
            print(message)
            self.send_to_thread(device.CONVEYER,message+'\n')
            