from flask import Flask, url_for, render_template, request, redirect
from module.connect_Factory import FactoryConnectMaster

app = Flask( __name__ )
key=True
th=FactoryConnectMaster()
@app.route( "/" )
def home():
    global key
    print("check")
    if(key):
        FactoryConnectMaster.connect()
        key=False
        th.start()
    return render_template( 'test.html' )

@app.route("/send/<message>")
def send(message):
    FactoryConnectMaster.send_message(message)
    return render_template( 'test.html' )

if __name__ == "__main__":
    
    app.run( host = "0.0.0.0", port = 8080, debug = True )
    
