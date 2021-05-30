import flask 
from flask import render_template, Response
from flask.globals import request
from datetime import datetime
import math
import time
import json 
import os 
app=flask.Flask(__name__)
timeleft = -1
settime = -1
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
    global timeleft, settime
    if request.method == "POST":
        timeleft = int(request.form['settime']) * 60 
        settime = timeleft//60
    return render_template("countingdown.html")

@app.route('/viewlogs')
def viewlogs():
    return render_template("logs.html")

@app.route('/intolog', methods=['GET', 'POST'])
def intolog():
    print(request.form['desc'])
    if os.path.exists("data.json"):
        with open("data.json") as datafile:
            savedata = json.load(datafile)
    else:
        savedata = {}
        savedata["id"] = 0
    
    id=savedata["id"]
    savedata["id"]+=1
    savedata[id] = dict( {
        "desc": request.form["desc"],
        "enddate": str(datetime.now()),
        "duration": settime
    })
    with open("data.json", "w+") as datafile:
        json.dump(savedata, datafile)

    return render_template("index.html")

app.run(host="0.0.0.0", port=8080, debug=True)

