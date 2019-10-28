from flask import Flask, url_for, render_template, request, redirect

app = Flask( __name__ )


@app.route( "/" )
def login():
    	return render_template( 'login.html' )

@app.route('/base',methods=['GET', 'POST'])
def base():
    return render_template('base.html')

@app.route( "/detail", methods = [ 'GET', 'POST' ] )
def detail():
    if request.method == 'GET':
        return render_template( "detail.html" )

@app.route( "/modify_weight", methods = [ 'GET', 'POST' ] )
def modify_weight():
    if request.method == 'GET':
        return render_template( "modify_weight.html" )

@app.route( "/modify_error", methods = [ 'GET', 'POST' ] )
def modify_error():
    if request.method == 'GET':
        return render_template( "modify_error.html" )

@app.route( "/modify_product", methods = [ 'GET', 'POST' ] )
def modify_product():
    if request.method == 'GET':
        return render_template( "modify_product.html" )

if __name__ == "__main__":
    app.run( host = "0.0.0.0", port = 8080, debug = True )
