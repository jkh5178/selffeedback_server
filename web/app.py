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
FactoryConnectMaster.connect()
def push_data():
    global socket_io
    global db
    global factory_connecter
    while True :
        
        #양품/불량품 데이터
        sql="select (select target_product from factory.product where no = 1)as target,count(case when result=1 then 1 end) as good, count(case when result=0 then 1 end) as bad from factory.log"
        main_head_data=db.read_data_dataframe(sql)
        send_target_weight_data=main_head_data.to_dict()

        socket_io.emit('head_data',send_target_weight_data,broadcast=True)#다른 데이터 전송
        #그래프 데이터
        sql="select count(*) as num, date from log group by date"
        chart_data=db.read_data_dataframe(sql)
        send_chart_data=chart_data.to_dict()
        socket_io.emit('new',send_chart_data,broadcast=True)#그래프 데이터

        
        FactoryConnectMaster.send_message("c")#
        socket_io.emit('device',FactoryConnectMaster.check_device(),broadcast=True)#기기 정보

        socket_io.emit('remain',FactoryConnectMaster.check_remain(),broadcast=True)#기기 정보
        socket_io.emit('test',"123456",broadcast=True)
        time.sleep(1)

push_data_thread=Thread(target=push_data)
factory_connecter=FactoryConnectMaster()
factory_connecter.start()
@app.route("/")
def main():
    global push_data_thread
    global factory_connecter

    if not push_data_thread.isAlive():
        push_data_thread.start()

    if not factory_connecter.isAlive():
        factory_connecter.start()


    return render_template('main.html')

@app.route( "/management", methods = [ 'GET', 'POST' ] )
def modify():
    if request.method == 'GET':
        return render_template( "management.html" )

@app.route("/start")
def send_start():
    global factory_connecter
    FactoryConnectMaster.send_message('s')
    return redirect('/')

@app.route("/end")
def send_end():
    global factory_connecter
    FactoryConnectMaster.send_message('e')
    return redirect('/')

@app.route("/inputdata" , methods = [ 'GET', 'POST' ] )
def input_data():
    weight = request.form["weight"]
    error_range = request.form["error_range"]
    
    time_sql = "(select factory.setting_value.open_time from factory.setting_value, factory.log where factory.log.weight = "+weight+" and factory.log.settingnum = factory.setting_value.no order by factory.log.no desc limit 1)"
    check_time = db.read_data_dataframe(time_sql).to_dict()["open_time"]
    if check_time == {}:
        open_time = str(2000)
    else:
        open_time = str(db.read_data_dataframe(time_sql).to_dict()["open_time"][0])
    
    
    input_sql = "insert into factory.setting_value(open_time,target_weight,target_range) values("+open_time+","+weight+","+error_range+")"
    db.input_data(input_sql)
    return redirect('/management')


if __name__ == "__main__":
    socket_io.run( app=app,host='0.0.0.0', port = 8080, debug = True )
