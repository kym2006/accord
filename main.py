import flask 
from flask import render_template
from flask.globals import request
import math
import time
app=flask.Flask(__name__)
@app.route('/')
def root():
    return render_template("index.html")


app.run(host="0.0.0.0", port=8080, debug=True)

