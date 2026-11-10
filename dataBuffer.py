import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import localCredentials
import numpy as np
import json
from json import JSONEncoder
import spiker
from datetime import datetime, timedelta

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
    def __init__(self,tim,brd=3,dev="FungalFrequencies_7483aff9d108",step=10,start_date=-1):
        global queryFS

        self.count = 0
        self.querry = queryFS
        self.min = 0
        self.max = 0
        
        self.updateStep = -1
        self.time = tim
        self.device = dev
        self.board = brd
        self.step = step

        self.sk = [spiker.spiker(), #1
                    spiker.spiker(),#2
                    spiker.spiker(),#3
                    spiker.spiker(),#4
                    spiker.spiker(),#5
                    spiker.spiker(),#6
                    spiker.spiker(),#7
                    spiker.spiker()]#8

        
        self.lenSpike = 7
        self.Update = 0
        self.spikeWord = ["","","","","","","","",""]


        self.oldData = False
        # Aktuelles Datum und Uhrzeit
        if( start_date != -1):
            self.current_date = datetime.now()
            # Differenz in Sekunden berechnen
            self.delta_seconds = int((self.current_date - start_date).total_seconds())
            self.oldData = True

        self.data = self.loadData(self.time)
        if(len(self.data[0]) > self.lenSpike):
            self.Update = self.lenSpike + 1


    def getJSON(self):
        numpyData = {   "board":self.board,  
                        "device": self.device, 
                        "data": self.data}
        return(json.dumps(numpyData, cls=NumpyArrayEncoder))


    def getTime(self, oldData, interval):
        if oldData:
            startt = -int((self.delta_seconds  - ( datetime.now() - self.current_date).total_seconds()))
            stoptt = -int((self.delta_seconds  + interval - ( datetime.now() - self.current_date).total_seconds()))
            starttime = "{}s, stop:{}".format(startt,stoptt)
            # print("time start: {}, stop: {} string:{}".format(startt,stoptt, starttime))
        else:
            starttime = interval 

        return starttime

    def loadData(self, interval):
        query = self.querry.format(time=self.getTime(self.oldData, interval),
                                   board=self.board, device=self.device, step=self.step)
        return self.fetchData(query)

    def update(self):
        newData = self.loadData(self.updateStep)
        sample_index = next((i for i, value in enumerate(newData[0]) if value is not None), None)
        if sample_index is None:
            return

        if not self.data[0]:
            # A board can start sending after the server has initialized its buffers.
            self.data = self.loadData(self.time)
        else:
            self.data = [
                [incoming[sample_index] if sample_index < len(incoming) else None, *previous[:-1]]
                for incoming, previous in zip(newData, self.data)
            ]

        self.Update += 1
        self.calcSpikes()

    def calcSpikes(self):
        if(self.Update > self.lenSpike):
            self.Update = 0
            values = [value for channel in self.data for value in channel if value is not None]
            if values:
                self.min = min(values)
                self.max = max(values)
            for i in range(8):
            
                if(len(self.data[i])> self.lenSpike):
                    arr = self.data[i][0:self.lenSpike]
                    if not None in arr:
                        self.spikeWord[i] = self.sk[i].calcSpikes(arr)

            
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


