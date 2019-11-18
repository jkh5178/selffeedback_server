from socket import *
import time
import threading

class FactoryConnectMaster(threading.Thread):
    HOST="localhost"
    PORT=8090
    conn = None
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        self.connected=False
        while True:
            while not self.connected:
                try:
                    print(self.connected)
                    FactoryConnectMaster.connect()
                    self.connected=True
                    print(self.connected)
                except:
                    print("연결실패...")
                    time.sleep(2)
            else:
                while True:
                    try:
                        print(self.conn.recv(32))
                    except:
                        FactoryConnectMaster.conn.close()
                        self.connected=False
                        break

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