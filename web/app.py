from flask import Flask, url_for, render_template, request, redirect

app = Flask( __name__ )


@app.route("/")
def main():
    return render_template('main.html')

@app.route( "/management", methods = [ 'GET', 'POST' ] )
def modify():
    if request.method == 'GET':
        return render_template( "management.html" )

if __name__ == "__main__":
    app.run( host = "0.0.0.0", port = 8080, debug = True )
