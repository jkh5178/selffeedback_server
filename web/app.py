from flask import Flask, url_for, jsonify,render_template, request, redirect
from subprocess import call
from flask_socketio import SocketIO, send
from module.DB import Db
import time
from threading import Thread
db=Db()

app = Flask( __name__ )
app.secret_key = "mysecret"
socket_io = SocketIO(app)

def push_data():
    global socket_io
    
    global db
    while True :
        sql="select count(*) as num, date from log group by date"
        data=db.read_data_dataframe(sql)
        send_data=data.to_dict()
        print(data)
        socket_io.emit('new',send_data,broadcast=True)
        time.sleep(10)

push_data_thread=Thread(target=push_data)

@app.route("/")
def main():
    global push_data_thread
    if not push_data_thread.isAlive():
        push_data_thread.start()
    return render_template('main.html')

@app.route( "/management", methods = [ 'GET', 'POST' ] )
def modify():
    if request.method == 'GET':
        return render_template( "management.html" )



if __name__ == "__main__":
    socket_io.run( app=app, port = 8080, debug = True )
