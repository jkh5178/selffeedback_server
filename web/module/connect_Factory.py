from socket import *
import time
import threading
from module.factory_enum import device

class FactoryConnectMaster(threading.Thread):
    HOST="localhost"
    PORT=8090
    conn = None
    current_time=0
    device_list=[]
    def __init__(self):
        threading.Thread.__init__(self)
        self.connected=True

    def run(self):
        
        while True:
            while not self.connected:
                try:
                    print(self.connected)
                    FactoryConnectMaster.connect()
                    self.connected=True
                    print(self.connected)
                except Exception:
                    print("연결실패...")
                    time.sleep(2)
            
            while True:
                try:
                    content=FactoryConnectMaster.conn.recv(32)
                    message=str(content)[1:-3].strip("'")
                    messages=message.split(";")
                    if messages[0]=="device":
                        FactoryConnectMaster.device_list=list(eval(messages[1]))
                    elif messages[0]=="remian":
                        pass
                except Exception as err:
                    print(err)
                    FactoryConnectMaster.conn.close()
                    self.connected=False
                    break
    @classmethod
    def check_device(cls):
        return cls.device_list
    
    @classmethod
    def connect(cls):
        cls.conn = socket(AF_INET, SOCK_STREAM)
        print(cls.conn)
        print("연결시도...")
        cls.conn.connect((cls.HOST,cls.PORT))
        cls.conn.send('master'.encode())
        print("start!!")
        

    @classmethod
    def send_message(cls,message):
        cls.conn.send(str(message).encode())