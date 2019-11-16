from flask import Flask, url_for, jsonify,render_template, request, redirect
from subprocess import call
from flask_socketio import SocketIO, send
from module.DB import Db
import time
from threading import Thread
from module.connect_Factory import FactoryConnectMaster
from threading import Event
db=Db()
app = Flask( __name__ )
app.secret_key = "mysecret"
socket_io = SocketIO(app,cors_allowed_origins="*")

def push_data():
    global socket_io
    global db

    while True :
        sql="select count(*) as num, date from log group by date"
        data=db.read_data_dataframe(sql)
        send_data=data.to_dict()
        print(data)
        socket_io.emit('new',send_data,broadcast=True)
        time.sleep(1)

push_data_thread=Thread(target=push_data)
factory_connecter=FactoryConnectMaster()
@app.route("/")
def main():
    global push_data_thread
    #global factory_connecter
    #if not factory_connecter.isAlive():
    #    FactoryConnectMaster.connect()
    #    factory_connecter.start()
    if not push_data_thread.isAlive():
        push_data_thread.start()
    return render_template('main.html')

@app.route( "/management", methods = [ 'GET', 'POST' ] )
def modify():
    if request.method == 'GET':
        return render_template( "management.html" )

@app.route("/start")
def send_start():
    global factory_connecter
    factory_connecter.send_message('s')
    return render_template('main.html')

@app.route("/end")
def send_end():
    global factory_connecter
    factory_connecter.send_message('e')
    return render_template('main.html')

if __name__ == "__main__":
    socket_io.run( app=app,host='0.0.0.0', port = 8080, debug = True )
