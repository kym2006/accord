import flask
from flask import render_template, Response
from flask.globals import request
from datetime import datetime, timedelta
import math
import time
import json
import os
app = flask.Flask(__name__)
timeleft = 0
settime = -1

def getdata(): # this function loads the data file and initiates the dictionary properly 
    if os.path.exists("data.json"):
        with open("data.json") as datafile:
            savedata = json.load(datafile)
    else:
        savedata = {}
        savedata["id"] = 0
        savedata["tags"] = []
    if "tags" not in savedata:
        savedata["tags"] = [] 
    if "id" not in savedata:
        savedata["id"] = 0 
    return savedata 

@app.route('/') # root view
def root():
    return render_template("index.html")

@app.route('/settings') # settings page
def settings():
    savedata = getdata()
    return render_template("settings.html", tags=savedata["tags"])


@app.route('/done') # makes the popup show up in the root view
def done():
    savedata = getdata()
    return render_template('index.html', done=1, tags=savedata["tags"])


@app.route('/addtag', methods=["POST"]) # posting to database to add a tag
def addtag():
    savedata = getdata()
    if request.form["newtag"] not in savedata["tags"]:
        savedata["tags"].append(request.form["newtag"])
    with open("data.json", "w+") as datafile:
        json.dump(savedata, datafile)

    return render_template("settings.html", tags=savedata["tags"])


@app.route('/changepic', methods=["POST"]) # changing the picture. The picture will just override the existing background picture
def changepic():
    savedata = getdata()
    request.files['file1'].save("static/notsogeneric1.jpg")
    return render_template("settings.html", tags=savedata["tags"])

@app.route('/time_feed') # this function is called once per second and will update the timer 
def time_feed():
    global timeleft
    timeleft = timeleft - 1
    if timeleft <= -1:
        timeleft = 0

    def generate():
        global timeleft

        return str(timeleft)  # return also will work
    return Response(generate(), mimetype='text')


@app.route('/loadtime', methods=['GET', 'POST']) # This starts the timer. If the time is 0, then it'll return the root view
def loadtime():
    global timeleft, settime
    if request.method == "POST":
        timeleft = int(request.form['settime']) * \
            60 + int(request.form['settimesec'])
        settime = timeleft
    else:
        if timeleft == 0:
            return render_template("index.html")
    return render_template("countingdown.html")


@app.route('/resettimer', methods=['GET', 'POST']) # this resets the timer and redirects to the homepage
def resettimer():
    global timeleft
    timeleft = 0
    return flask.redirect("/")


@app.route('/viewlogs')
def viewlogs():
    savedata = getdata()
    for k, v in savedata.items():
        if type(v) == type(savedata):
            v['enddate'] = datetime.strptime(
                v['enddate'], '%Y-%m-%d %H:%M:%S.%f') # This saves the datetime in the following format 
    savedata = dict(list(savedata.items())[1:]) # This discards the id field
    info = dict()
    for k, v in savedata.items():
        if type(v) != type(dict()):
            continue
        start = v['enddate'] - timedelta(seconds=settime)
        datestr = start.strftime("%A, %d %B %Y")
        if datestr not in info:
            info[datestr] = []
        di = dict()
        di['starttime'] = start.strftime("%H:%M")
        di['endtime'] = v['enddate'].strftime("%H:%M")
        di['duration'] = str(v['duration']//3600).rjust(2, '0') + ":" + str(
            (v['duration'] % 3600)//60).rjust(2, '0') + ":" + str(v['duration'] % 60).rjust(2, '0') # padding right to make it look proper
        di['desc'] = v['desc']
        info[datestr].append(di)
    return render_template("logs.html", logs=reversed(list(info.items()))) # we pass the logs in reverse so the things with a later time will appear later


@app.route('/intolog', methods=['GET', 'POST'])
def intolog():
    if settime == -1:
        return render_template("index.html")
    savedata = getdata()
    id = savedata["id"]
    savedata["id"] += 1
    desc = request.form["desc"]
    for k, v in request.form.items():
        if k[:3] == "tag" and v=="on":
            desc += f"| {k[3:]} " # the first 3 characters are tag which are useless
    savedata[id] = dict({
        "desc": desc,
        "enddate": str(datetime.now()),
        "duration": settime
    })
    with open("data.json", "w+") as datafile:
        json.dump(savedata, datafile)

    return render_template("index.html")

@app.route('/removetag', methods=['POST'])
def removetag():
    savedata = getdata()
    savedata["tags"].remove(request.json["value"])
    with open("data.json", "w+") as datafile:
        json.dump(savedata, datafile)

    return render_template("settings.html")
app.run(debug=True)