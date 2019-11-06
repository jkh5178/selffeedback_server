from socket import *

HOST='127.0.0.1'

c = socket(AF_INET, SOCK_STREAM)
print ('connecting....')
c.connect((HOST,8090))
print ('ok')
c.send('bm')
while 1:
        data = input()
        c.send(data)