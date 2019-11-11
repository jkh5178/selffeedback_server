from device.Thread_client import Client

class CupDispensor(Client):
    def __init__(self,index, client, mainThread):
        Client.__init__(self,index,client,mainThread)
    def do_job(self):
        while True:
            pass