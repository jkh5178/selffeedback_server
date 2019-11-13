from socket import *
import time
import threading

class FactoryConnectMaster(threading.Thread):
    HOST="localhost"
    PORT=8090
    conn = socket(AF_INET, SOCK_STREAM)
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while True:
            print(self.conn.recv(32))

    @classmethod
    def connect(cls):
        cls.conn.connect((cls.HOST,cls.PORT))
        cls.conn.send('master'.encode())
        print("start!!")
        

    @classmethod
    def send_message(cls,message):
        cls.conn.send(str(message).encode())