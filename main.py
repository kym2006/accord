import flask 
from flask import render_template, Response
from flask.globals import request
from datetime import datetime, timedelta
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
    if os.path.exists("data.json"):
        with open("data.json") as datafile:
            savedata = json.load(datafile)
    else:
        savedata = {}
        savedata["id"] = 0
    for k, v in savedata.items():
        if type(v) == type(savedata):
            v['enddate'] = datetime.strptime(v['enddate'], '%Y-%m-%d %H:%M:%S.%f')
    savedata = dict(list(savedata.items())[1:])
    info = dict() 
    print(savedata)
    for k, v in savedata.items():
        start = v['enddate'] - timedelta(minutes=settime)
        datestr = start.strftime("%A, %d %B %Y")
        if datestr not in info:
            info[datestr] = [] 
        di = dict()
        di['starttime'] = start.strftime("%H:%M")
        di['duration'] = v['duration']
        di['desc'] = v['desc'] 
        info[datestr].append(di)
    print(info)
    return render_template("logs.html", logs=info)

@app.route('/intolog', methods=['GET', 'POST'])
def intolog():
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

