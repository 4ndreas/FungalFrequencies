# https://cabreraalex.medium.com/svelte-js-flask-combining-svelte-with-a-simple-backend-server-d1bc46190ab9

import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from flask import Flask, send_from_directory, render_template , request,jsonify,json
from flask_cors import CORS, cross_origin
import random
import pandas as pd
import influxGet



app = Flask(__name__)
# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})



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
    return(pd.Series(influxGet.fetchData(influxGet.query3)).to_json(orient='values'))


if __name__ == "__main__":
    app.run(debug=True)