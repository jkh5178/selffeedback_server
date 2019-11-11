from Thread_client import Client
from factory_enum import device
class Master(Client):
    def __init__(self,index,client,mainThread):
        Client.__init__(self,index,client,mainThread)
    def do_job(self):
        while True:
            self.content=self.client.recv(32)
            message=str(self.content)[1:].strip("'")
            print(str(message))
            if message=='s':
                self.tm.start()
            elif message=='e':
                self.tm.stop()
            elif message=='c':
                print(len(self.tm.thread_dic))
