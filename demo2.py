import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import matplotlib.pyplot as plt
import numpy
import numpy as np
from statsmodels.tsa import stattools
from scipy.signal import butter, lfilter, freqz
import localCredentials
import spiker


client = influxdb_client.InfluxDBClient(url=localCredentials.url, token=localCredentials.ffToken, org=localCredentials.org)

query_api = client.query_api()


# 2024-08-11 11:50:19
# 2024-08-11 12:22:40

query = """from(bucket: "fungalF")
  |> range(start: 2024-08-11T09:50:00.000Z, stop: 2024-08-11T10:22:00.000Z)
  |> filter(fn: (r) => r["_measurement"] == "adcData")
  |> filter(fn: (r) => r["ADC"] == "ADS1115")
  |> filter(fn: (r) => r["_field"] == "CH_3")
  |> filter(fn: (r) => r["board"] == "4")
  |> filter(fn: (r) => r["device"] == "FungalFrequencies_7483aff9d108")"""

# spikes
query2 = """from(bucket: "fungalF")
  |> range(start: 2024-08-11T09:50:00.000Z, stop: 2024-08-11T10:28:00.000Z)
  |> filter(fn: (r) => r["_measurement"] == "adcData")
  |> filter(fn: (r) => r["ADC"] == "ADS1115")
  |> filter(fn: (r) => r["_field"] == "CH_3")
  |> filter(fn: (r) => r["board"] == "4")
  |> filter(fn: (r) => r["device"] == "FungalFrequencies_7483aff9d108")
  |> aggregateWindow(every: 10s, fn: mean, createEmpty: true)"""

#noise no spikes
query3 = """from(bucket: "fungalF")
  |> range(start: 2024-08-11T09:00:00.000Z, stop: 2024-08-11T09:20:00.000Z)
  |> filter(fn: (r) => r["_measurement"] == "adcData")
  |> filter(fn: (r) => r["ADC"] == "ADS1115")
  |> filter(fn: (r) => r["_field"] == "CH_3")
  |> filter(fn: (r) => r["board"] == "4")
  |> filter(fn: (r) => r["device"] == "FungalFrequencies_7483aff9d108")
  |> aggregateWindow(every: 10s, fn: mean, createEmpty: true)"""

# ONE spike
query4 = """from(bucket: "fungalF")
  |> range(start: 2024-08-11T08:00:30.000Z, stop: 2024-08-11T09:10:00.000Z)
  |> filter(fn: (r) => r["_measurement"] == "adcData")
  |> filter(fn: (r) => r["ADC"] == "ADS1115")
  |> filter(fn: (r) => r["_field"] == "CH_3")
  |> filter(fn: (r) => r["board"] == "4")
  |> filter(fn: (r) => r["device"] == "FungalFrequencies_7483aff9d108")
  |> aggregateWindow(every: 10s, fn: mean, createEmpty: true)"""

# TOW words
query5 = """from(bucket: "fungalF")
  |> range(start: 2024-08-11T10:30:00.000Z, stop: 2024-08-11T10:45:00.000Z)
  |> filter(fn: (r) => r["_measurement"] == "adcData")
  |> filter(fn: (r) => r["ADC"] == "ADS1115")
  |> filter(fn: (r) => r["_field"] == "CH_3")
  |> filter(fn: (r) => r["board"] == "4")
  |> filter(fn: (r) => r["device"] == "FungalFrequencies_7483aff9d108")
  |> aggregateWindow(every: 5s, fn: mean, createEmpty: true)"""


tables = query_api.query(query4, org="surreallabor")

results = []
results0 = []
for table in tables:
  for record in table.records:
    # t = record.get_time().second*1000000 + record.get_time().microsecond
    # results.append((record.get_field(), record.get_value(), t, record.get_time()))

    if(record.get_field() == 'CH_3'):
      results0.append((record.get_value()))


lPlot = len(results0)
t = np.arange(0, lPlot, 1)

# spikes = spiker.getSpinkes(results0)

sk = spiker.spiker()
words = sk.getSpikes(results0)
print(words)


plt.plot(t,results0)
plt.show()
