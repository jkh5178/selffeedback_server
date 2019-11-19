from module.Thread_client import Client
from module.factory_enum import device
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
                self.send_to_device('start')
            elif message=='e':
                self.tm.stop()
                self.send_to_device('end')
            elif message=='c':
                send_list=[]
                connect_device_list=list(self.tm.thread_dic.keys())
                print(list(self.tm.thread_dic.keys()))
                print(len(self.tm.thread_dic))
                for i in connect_device_list:
                    send_list.append(i.value)
                self.send_to_device("device;"+str(send_list))
