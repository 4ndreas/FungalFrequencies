# https://cabreraalex.medium.com/svelte-js-flask-combining-svelte-with-a-simple-backend-server-d1bc46190ab9

import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from flask import Flask, send_from_directory, render_template , request,jsonify,json ,redirect, url_for
from flask_cors import CORS, cross_origin
from flask_apscheduler import APScheduler
from flask import g
import random
import pandas as pd
import influxGet
import dataBuffer
import numpy as np

class Config(object):
    SCHEDULER_API_ENABLED = True


# create app
app = Flask(__name__)
app.config.from_object(Config())
# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})


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



dataBuff = [dataBuffer.dataBuffer(buffertime, boardIDs[0], boardDevs[0],bufferstep), #0 Oben board 1
            dataBuffer.dataBuffer(buffertime, boardIDs[1], boardDevs[1],bufferstep), #1 Oben board 2
            dataBuffer.dataBuffer(buffertime, boardIDs[2], boardDevs[2],bufferstep), #2 Oben board 3
            dataBuffer.dataBuffer(buffertime, boardIDs[3], boardDevs[3],bufferstep), #3 Oben board 4

            dataBuffer.dataBuffer(buffertime, boardIDs[4], boardDevs[4] ,bufferstep), #4 Links board 1
            dataBuffer.dataBuffer(buffertime, boardIDs[5], boardDevs[5],bufferstep), #5 Links board 2
            dataBuffer.dataBuffer(buffertime, boardIDs[6], boardDevs[6],bufferstep), #6 Links board 3
            dataBuffer.dataBuffer(buffertime, boardIDs[7], boardDevs[7],bufferstep), #7 Links board 4

            dataBuffer.dataBuffer(buffertime, boardIDs[8], boardDevs[8],bufferstep), #8 Unten board 1
            dataBuffer.dataBuffer(buffertime, boardIDs[9], boardDevs[9],bufferstep), #9 Unten board 2
            dataBuffer.dataBuffer(buffertime, boardIDs[10], boardDevs[10],bufferstep), #10 Unten board 3
            dataBuffer.dataBuffer(buffertime, boardIDs[11], boardDevs[11],bufferstep), #11 Unten board 4

            dataBuffer.dataBuffer(buffertime, boardIDs[12], boardDevs[12],bufferstep), #12 Rechts board 1
            dataBuffer.dataBuffer(buffertime, boardIDs[13], boardDevs[13],bufferstep), #13 Rechts board 2
            dataBuffer.dataBuffer(buffertime, boardIDs[14], boardDevs[14],bufferstep), #14 Rechts board 3
            dataBuffer.dataBuffer(buffertime, boardIDs[15], boardDevs[15],bufferstep)] #15 Rechts board 4

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

        q = influxGet.queryFS.format(time = time, board = board, device = device, step = step)
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

        q = influxGet.queryFS.format(time = time, board = boardIDs[board], device = boardDevs[board], step = step)
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