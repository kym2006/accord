import flask 
from flask import render_template, Response
from flask.globals import request
from datetime import datetime
import math
import time
app=flask.Flask(__name__)
timeleft = -1
@app.route('/')
def root():
    return render_template("index.html")

@app.route('/done') 
def done():
    return render_template('index.html', done=1)

@app.route('/time_feed')
def time_feed():
    global timeleft 
    timeleft = timeleft - 1
    if timeleft <= -1:
        timeleft = 0
    def generate():
        global timeleft 
            
        return str(timeleft)  # return also will work
    return Response(generate(), mimetype='text') 

@app.route('/loadtime', methods=['GET', 'POST'])
def loadtime():
    global timeleft 
    if request.method == "POST":
        timeleft = int(request.form['settime']) * 60 
    return render_template("countingdown.html")

app.run(host="0.0.0.0", port=8080, debug=True)

