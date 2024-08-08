import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import matplotlib.pyplot as plt
import numpy
import numpy as np
from statsmodels.tsa import stattools
from scipy.signal import butter, lfilter, freqz

# token = os.environ.get("INFLUXDB_TOKEN")
token = "1HIwj5wtCLVN-cHDCE63ELql1BY90rbe6407HU-Enx-A4yNZ-jQfbZgFHWfGe1xGJKcYdCibZisrpI7tDq0fYQ=="
org = "surreallabor"
url = "http://192.168.2.10:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()


# query = """from(bucket: "surreallaborData")
#   |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
#   |> filter(fn: (r) => r["_measurement"] == "adcData")
#   |> filter(fn: (r) => r["ADC"] == "ADS1115")
#   |> filter(fn: (r) => r["_field"] == "CH_0" or r["_field"] == "CH_1" or r["_field"] == "CH_2" or r["_field"] == "CH_3" or r["_field"] == "CH_4" or r["_field"] == "CH_5" or r["_field"] == "CH_6" or r["_field"] == "CH_7")
#   |> filter(fn: (r) => r["board"] == "0")
#   |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
#   |> yield(name: "mean")"""

# query = """from(bucket: "surreallaborData")
#  |> range(start: -2s)
#  |> filter(fn: (r) => r._measurement == "adcData")
#  |> filter(fn: (r) => r.board == "0")"""

# 2024-06-20 00:46:37
# 2024-06-20 03:05:20
# start_string = '2024-06-20 00:46:37'
# stop_string = '2024-06-20 03:05:20'

# starttime = datetime.strptime(start_string, '%Y-%m-%d %H:%M:%S')
# stoptime = datetime.strptime(stop_string, '%Y-%m-%d %H:%M:%S')

# range(start: 2024-06-20 00:46:37, stop: 2024-06-20 03:05:20)
#   |> range(start: -10s)
# range(start: 2024-06-19T22:46:37.000Z



# |> range(start: 2024-06-20T01:19:20.000Z, stop: 2024-06-20T01:37:31.000Z)
# |> range(start: 2024-06-20T00:46:37.000Z, stop: 2024-06-20T03:05:20.000Z)

# Test 1
#  |> range(start: 2024-06-19T23:19:20.000Z, stop: 2024-06-19T23:37:31.000Z)

# Test 2
#  |> range(start: 2024-06-20T00:46:37.000Z, stop: 2024-06-20T03:05:20.000Z)

query = """from(bucket: "surreallaborData")
  |> range(start: 2024-06-20T00:46:37.000Z, stop: 2024-06-20T03:05:20.000Z)
  |> filter(fn: (r) => r["_measurement"] == "adcData")
  |> filter(fn: (r) => r["ADC"] == "ADS1115")
  |> filter(fn: (r) => r["_field"] == "CH_0" or r["_field"] == "CH_1" or r["_field"] == "CH_2" or r["_field"] == "CH_3" or r["_field"] == "CH_4" or r["_field"] == "CH_6" or r["_field"] == "CH_5" or r["_field"] == "CH_7")
  |> filter(fn: (r) => r["device"] == "SporeSense_9c4b59ebd724")"""




tables = query_api.query(query, org="surreallabor")

results = []
results0 = []
for table in tables:
  for record in table.records:
    # t = record.get_time().second*1000000 + record.get_time().microsecond
    # results.append((record.get_field(), record.get_value(), t, record.get_time()))

    if(record.get_field() == 'CH_4'):
      results0.append((record.get_value()))
    # print(record)

# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')


# record.get_time().microsecond
def autocorr(x):
    result = numpy.correlate(x, x, mode='full')
    return result[result.size//2:]

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# def autocorrelation (x) :
#     """
#     Compute the autocorrelation of the signal, based on the properties of the
#     power spectral density of the signal.
#     """
#     xp = x-np.mean(x)
#     f = np.fft.fft(xp)
#     p = np.array([np.real(v)**2+np.imag(v)**2 for v in f])
#     pi = np.fft.ifft(p)
#     return np.real(pi)[:x.size/2]/np.sum(xp**2)

# print(results0)

spike = [0,0,0,1,0,0,0]
spike2 = [0,0,0,0,0,1,0]
spike3 = [0,1,0,0,0,0,0]
# spike2 = [0,0,0.2,0.6,0.2,0,0]
# spike = [0,0,0.5,0,0.5,0,0]
# spike = [0,0,-0.1,0.8,-0.1,0,0]
# spike = [0,0,-0.5,2,-0.5,0,0]
# spike = [0,0,0.1,0.8,0.1,0,0]
# spike = [0,0.1,0.2,0.4,0.2,0.1,0]

lenSpike = len(spike)
# spike = [1,1,1,2,1,1,1]
# spike = [-2,-2,-2,-1,-2,-2,-2]
akrSpike = stattools.acf(spike)
correlation = []
autocorrelation = []
autocorrelation2 = []
spikes = []
filtered = []
spikeString = ""
stringCounter = 0
zeroCounter = 0
words = []

zerosDist = 20
zeroThr = 1



# Filter requirements.
order = 4
fs = 30.0       # sample rate, Hz
cutoff = 10  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
# results0 = butter_lowpass_filter(results0, cutoff, fs, order)

results1 = np.copy(results0)
results0 = np.multiply(results0,-1)

i = 0
while i <  len(results0)-lenSpike:
  arr = results0[i:i+lenSpike]

  corr = numpy.correlate(spike,arr, mode='same')
  correlation.extend(corr)
  autocorrelation.extend( arr - corr )

  s = np.clip(corr - arr,-2,0)

  corr2 = numpy.correlate(spike2,arr, mode='same')
  s = np.clip(s + np.clip(corr2 - arr,-2,0),-2,0)

  corr3 = numpy.correlate(spike3,arr, mode='same')
  s = np.clip(s + np.clip(corr3 - arr,-2,0),-2,0)

  f = np.piecewise(s, [s > -zeroThr, s <= -zeroThr], [0, 1])
  spikes.extend(s)
  filtered.extend(f)

  for j in range(0,len(f)):
    if f[j] == 1:
      if zeroCounter > 0:
        zeros = ''.join(chr(ord('0')) for i in range(zeroCounter))   
        spikeString += zeros

      spikeString += '1'
      zeroCounter = 0
      stringCounter = zerosDist
    else:
      if (stringCounter > 0):
        stringCounter -= 1
        zeroCounter += 1
      else:
        if spikeString != "":
          words.append(spikeString)
          print(spikeString)
          spikeString = ""
          zeroCounter = 0
  
  i+=lenSpike


lPlot = len(correlation)
t = np.arange(0, lPlot, 1)





# dhi = 0.3 - np.clip(autocorrelation,-1,0)
# dlo = 0.3 - np.clip(autocorrelation,-1,0)
# idx = dhi + dlo < 0
# the_rounded = the_list + np.where(idx, dhi, dlo)
# spikes = np.clip(autocorrelation,-1,0)
# filtered = np.piecewise(spikes, [spikes > -0.3, spikes <= -0.3], [0, 1])

# plt.plot(t,results0[0:len(correlation)],t,correlation,t,autocorrelation)

# plt.plot(t,results0[0:len(correlation)],t,filtered,t,spikes,t,autocorrelation)
plt.plot(t,results0[0:len(correlation)],t,filtered,t,spikes)
# plt.plot(t,results0[0:len(correlation)],t,filtered,t,y[0:len(correlation)])
# plt.plot(t,results0[0:len(correlation)],t,correlation)
plt.show()

# from(bucket: "surreallaborData")
#   |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
#   |> filter(fn: (r) => r["_measurement"] == "adcData")
#   |> filter(fn: (r) => r["ADC"] == "ADS1115")
#   |> filter(fn: (r) => r["_field"] == "CH_0" or r["_field"] == "CH_1" or r["_field"] == "CH_2" or r["_field"] == "CH_3" or r["_field"] == "CH_4" or r["_field"] == "CH_5" or r["_field"] == "CH_6" or r["_field"] == "CH_7")
#   |> filter(fn: (r) => r["board"] == "0")
#   |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
#   |> yield(name: "mean")