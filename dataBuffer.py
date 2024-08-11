import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import localCredentials
import numpy as np
import json
from json import JSONEncoder
import spiker

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
    
fileds = ['CH_0','CH_1','CH_2','CH_3','CH_4','CH_5','CH_6','CH_7']

queryFS = """from(bucket: "fungalF")
    |> range(start: {time}s)
    |> filter(fn: (r) => r["_measurement"] == "adcData")
    |> filter(fn: (r) => r["ADC"] == "ADS1115")
    |> filter(fn: (r) => r["_field"] == "CH_0" or r["_field"] == "CH_1" or r["_field"] == "CH_3" or r["_field"] == "CH_2" or r["_field"] == "CH_4" or r["_field"] == "CH_5" or r["_field"] == "CH_6" or r["_field"] == "CH_7")
    |> filter(fn: (r) => r["board"] == "{board}")
    |> filter(fn: (r) => r["device"] == "{device}")
    |> aggregateWindow(every: {step}s, fn: mean, createEmpty: true)"""

class dataBuffer:
    def __init__(self,tim,brd=3,dev="FungalFrequencies_7483aff9d108",step=10):
        global queryFS

        self.count = 0
        self.querry = queryFS
        
        self.updateStep = -1
        self.time = tim
        self.device = dev
        self.board = brd
        self.step = step

        self.sk = spiker.spiker()
        self.Update = 0
        self.spikeWord = ""


        # initial querry 
        s = self.querry.format(time = self.time, board = self.board, device = self.device, step = self.step)
        self.data = self.fetchData(s)

    def getJSON(self):
        numpyData = {   "board":self.board,  
                        "device": self.device, 
                        "data": self.data}
        return(json.dumps(numpyData, cls=NumpyArrayEncoder))


    def update(self):
        s = self.querry.format(time = self.updateStep, board = self.board, device = self.device, step = self.step)
        newData = self.fetchData(s)
        if(len(newData[0])>0):

            if(newData[0][0] == None):
                newData = np.delete(newData,0, axis=1)
            while (len(newData[0])>1):
                if(newData[0][0] == None):
                    newData = np.delete(newData,0, axis=1)
                if(len(newData[0])>1):
                    newData = np.delete(newData,len(newData[0])-1, axis=1)
                else:
                    break

            # roll array
            self.data= np.roll(self.data, (8, 1), axis=(0, 1))
            # remove last element what is now the first
            self.data = np.delete(self.data,0, axis=1)
            # add new data as first element
            self.data = np.insert(self.data, [0], newData, axis=1)
            
            # save update counter
            self.Update+=1
            self.calcSpikes()

    def calcSpikes(self):
        if(self.Update> self.sk.lenSpike):
            self.Update = 0
            for i in range(8):
                if(len(self.data[i])> self.sk.lenSpike):
                    self.spikeWord = self.sk.calcSpikes(self.data[i][0:self.sk.lenSpike])

            
    def fetchData(self,query):
        # token = os.environ.get("INFLUXDB_TOKEN")
        client = influxdb_client.InfluxDBClient(url=localCredentials.url, token=localCredentials.ffToken, org=localCredentials.org)
        query_api = client.query_api()

        tables = query_api.query(query, org=localCredentials.org)

        lx = len(fileds)

        results = [ [] for _ in range(lx)]
        for table in tables:
            for record in table.records:
                for i in range(lx):
                    if(record.get_field() == fileds[i]):
                        results[i].append((record.get_value()))    
        return results


