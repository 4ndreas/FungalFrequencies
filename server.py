# https://cabreraalex.medium.com/svelte-js-flask-combining-svelte-with-a-simple-backend-server-d1bc46190ab9

import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from flask import Flask, send_from_directory, render_template , request,jsonify,json
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

buffertime = -10*60
bufferstep = 5

dataBuff = [dataBuffer.dataBuffer(buffertime,2, "FungalFrequencies_7483aff9d108",bufferstep), # Oben board 1
            dataBuffer.dataBuffer(buffertime,3, "FungalFrequencies_7483aff9d108",bufferstep), # Oben board 2
            dataBuffer.dataBuffer(buffertime,4, "FungalFrequencies_7483aff9d108",bufferstep), # Oben board 3
            dataBuffer.dataBuffer(buffertime,5, "FungalFrequencies_7483aff9d108",bufferstep), # Oben board 4

            dataBuffer.dataBuffer(buffertime,2, "FungalFrequencies_944e71b3a3a0",bufferstep), # Links board 1
            dataBuffer.dataBuffer(buffertime,3, "FungalFrequencies_944e71b3a3a0",bufferstep), # Links board 2
            dataBuffer.dataBuffer(buffertime,4, "FungalFrequencies_944e71b3a3a0",bufferstep), # Links board 3
            dataBuffer.dataBuffer(buffertime,5, "FungalFrequencies_944e71b3a3a0",bufferstep), # Links board 4

            dataBuffer.dataBuffer(buffertime,2, "FungalFrequencies_10d1aff9d108",bufferstep), # Unten board 1
            dataBuffer.dataBuffer(buffertime,3, "FungalFrequencies_10d1aff9d108",bufferstep), # Unten board 2
            dataBuffer.dataBuffer(buffertime,4, "FungalFrequencies_10d1aff9d108",bufferstep), # Unten board 3
            dataBuffer.dataBuffer(buffertime,5, "FungalFrequencies_10d1aff9d108",bufferstep), # Unten board 4

            dataBuffer.dataBuffer(buffertime,2, "FungalFrequencies_50f776b3a3a0",bufferstep), # Rechts board 1
            dataBuffer.dataBuffer(buffertime,3, "FungalFrequencies_50f776b3a3a0",bufferstep), # Rechts board 2
            dataBuffer.dataBuffer(buffertime,4, "FungalFrequencies_50f776b3a3a0",bufferstep), # Rechts board 3
            dataBuffer.dataBuffer(buffertime,5, "FungalFrequencies_50f776b3a3a0",bufferstep)] # Rechts board 4

spikeWord = ""
spikeBoard = -1

@scheduler.task('interval', id='do_job_1', seconds=10, misfire_grace_time=900)
def job1():
    global dataBuff, spikeWord, spikeBoard

    print("update buffers")
    for i in range(len(dataBuff)):
        dataBuff[i].update()
        if(dataBuff[i].spikeWord != ""):
             print(dataBuff[i].spikeWord)


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
    print(x)
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
        
@app.route("/bdata")
def bdata():
    # Buffered Data
    board = request.args.get('b', default = 0, type = int)
    board = max(min(board,len(dataBuff)),1)-1

    return(dataBuff[board].getJSON())

@app.route("/bdata")
def spike():
    global spikeWord, spikeBoard
    spikeData = { "board": spikeBoard,  
                  "spikeWord": spikeWord}
    
    return(json.dumps(spikeData))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)