# https://cabreraalex.medium.com/svelte-js-flask-combining-svelte-with-a-simple-backend-server-d1bc46190ab9

import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from flask import Flask, send_from_directory, render_template , request,jsonify,json ,redirect, url_for
from flask_cors import CORS, cross_origin
from flask_apscheduler import APScheduler
from flask import g
import os
import random
import pandas as pd
import influxGet
import dataBuffer
import numpy as np
from datetime import datetime, timedelta

class Config(object):
    SCHEDULER_API_ENABLED = True


# create app
app = Flask(__name__)
app.config.from_object(Config())
# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})

oldData = os.environ.get("FUNGAL_HISTORY_MODE") == "1"
start_date = datetime(2024, 8, 17, 9)
buffer_start_date = start_date if oldData else -1

# Aktuelles Datum und Uhrzeit
current_date = datetime.now()

# Differenz in Sekunden berechnen
delta_seconds = int((current_date - start_date).total_seconds())

def getTime(oldData, interval):
    if oldData:
        startt = -int((delta_seconds  - ( datetime.now() - current_date).total_seconds()))
        stoptt = -int((delta_seconds  + interval - ( datetime.now() - current_date).total_seconds()))
        starttime = "{}s, stop:{}".format(startt,stoptt)
        # print("time start: {}, stop: {} string:{}".format(startt,stoptt, starttime))
    else:
        starttime = interval 

    return starttime

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

buffertime = -15*60
bufferstep = 5


boardIDs = [ 2,3,4,5,
             2,3,4,5,
             2,3,4,5,
             2,3,4,5 ]

boardDevs = [ "FungalFrequencies_7483aff9d108","FungalFrequencies_7483aff9d108","FungalFrequencies_7483aff9d108","FungalFrequencies_7483aff9d108",
             "FungalFrequencies_944e71b3a3a0","FungalFrequencies_944e71b3a3a0","FungalFrequencies_944e71b3a3a0","FungalFrequencies_944e71b3a3a0",
             "FungalFrequencies_10d1aff9d108","FungalFrequencies_10d1aff9d108","FungalFrequencies_10d1aff9d108","FungalFrequencies_10d1aff9d108",
             "FungalFrequencies_50f776b3a3a0","FungalFrequencies_50f776b3a3a0","FungalFrequencies_50f776b3a3a0","FungalFrequencies_50f776b3a3a0"]



dataBuff = [
    dataBuffer.dataBuffer(buffertime, board, device, bufferstep, buffer_start_date)
    for board, device in zip(boardIDs, boardDevs)
]

spikeWord = ""
spikeBoard = 0
spikeChannel = 0
gMin = 0
gMax = 0
spikeWordCount = 0

@scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
def job1():
    global dataBuff, spikeWord, spikeBoard, spikeChannel,spikeWordCount,gMin, gMax
    gMin = 0
    gMax = 0
    # print("update buffers")
    for i in range(len(dataBuff)):
        dataBuff[i].update()
        gMin = min(dataBuff[i].min,gMin)
        gMax = max(dataBuff[i].max,gMax)

        for j in range(8):
            if(dataBuff[i].spikeWord[j] != ""):  
                spikeWord = dataBuff[i].spikeWord[j]
                # spikeBoard = str(i) + "_" + str(j)
                spikeBoard = i
                spikeChannel = j
                dataBuff[i].spikeWord[j] = ""
                spikeWordCount +=1

                print("Board:" + str(i) + "_" + str(j) + " Data: " + spikeWord)


# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/dist', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/dist', path)

@app.route("/rand")
def hello():
    return str(random.randint(0, 100))

@app.route("/data")
def data():
    x = influxGet.fetchData(influxGet.query3)
    # print(x)
    return(pd.Series(x).to_json(orient='values'))

@app.route("/idata")
def idata():
    global dataBuff
    try:
        board = request.args.get('b', default = 5, type = int)
        time = request.args.get('t', default = -10, type = int)
        device = request.args.get('d', default = "FungalFrequencies_7483aff9d108", type = str)
        step = request.args.get('s', default = 1, type = int)

        q = influxGet.queryFS.format(time = getTime(oldData, time), board = board, device = device, step = step)
        return(pd.Series(influxGet.fetchData(q)).to_json(orient='values'))
    except:
        return([])

@app.route("/jdata")
def jdata():
    global dataBuff
    try:
        board = request.args.get('b', default = 0, type = int)
        time = request.args.get('t', default = -10, type = int)
        step = request.args.get('s', default = 1, type = int)

        board = max(min(board,len(dataBuff)-1),0)

        q = influxGet.queryFS.format(time = getTime(oldData, time), board = boardIDs[board], device = boardDevs[board], step = step)
        return(pd.Series(influxGet.fetchData(q)).to_json(orient='values'))
    except:
        return([])

@app.route("/bdata")
def bdata():
    # Buffered Data
    board = request.args.get('b', default = 0, type = int)
    board = max(min(board,len(dataBuff)-1),0)

    return(dataBuff[board].getJSON())

@app.route("/spike")
def spike():
    global spikeWord, spikeBoard,spikeChannel
    spikeData = { "board": spikeBoard,  
                  "channel": spikeChannel,
                  "spikeWord": spikeWord}
    
    return(json.dumps(spikeData))

@app.route("/api/stats")
def stats():
    global spikeWord, gMin, gMax, spikeWordCount
    spikeData = { "min": gMin,  
                  "max": gMax,
                  "wordCount": spikeWordCount,
                  "spikeWord": spikeWord}
    
    return(json.dumps(spikeData))

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    data = {"status": "success"}
    return data, 200


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)