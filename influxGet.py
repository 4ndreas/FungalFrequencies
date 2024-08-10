import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import localCredentials


fileds = ['CH_0','CH_1','CH_2','CH_3','CH_4','CH_5','CH_6','CH_7']


def fetchData(query):
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



query = """from(bucket: "surreallaborData")
|> range(start: 2024-06-20T00:46:37.000Z, stop: 2024-06-20T03:05:20.000Z)
|> filter(fn: (r) => r["_measurement"] == "adcData")
|> filter(fn: (r) => r["ADC"] == "ADS1115")
|> filter(fn: (r) => r["_field"] == "CH_0" or r["_field"] == "CH_1" or r["_field"] == "CH_2" or r["_field"] == "CH_3" or r["_field"] == "CH_4" or r["_field"] == "CH_6" or r["_field"] == "CH_5" or r["_field"] == "CH_7")
|> filter(fn: (r) => r["device"] == "SporeSense_9c4b59ebd724")"""


query2 = """from(bucket: "fungalF")
|> range(start: -10s)
|> filter(fn: (r) => r["_measurement"] == "adcData")
|> filter(fn: (r) => r["ADC"] == "ADS1115")
|> filter(fn: (r) => r["_field"] == "CH_0" or r["_field"] == "CH_1" or r["_field"] == "CH_2" or r["_field"] == "CH_3" or r["_field"] == "CH_4" or r["_field"] == "CH_5" or r["_field"] == "CH_6" or r["_field"] == "CH_7")
|> filter(fn: (r) => r["board"] == "2")
|> filter(fn: (r) => r["device"] == "FungalFrequencies_10d1aff9d108")"""


query3 = """from(bucket: "fungalF")
    |> range(start: -10s)
    |> filter(fn: (r) => r["_measurement"] == "adcData")
    |> filter(fn: (r) => r["ADC"] == "ADS1115")
    |> filter(fn: (r) => r["_field"] == "CH_0" or r["_field"] == "CH_1" or r["_field"] == "CH_3" or r["_field"] == "CH_2" or r["_field"] == "CH_4" or r["_field"] == "CH_5" or r["_field"] == "CH_6" or r["_field"] == "CH_7")
    |> filter(fn: (r) => r["board"] == "3")
    |> filter(fn: (r) => r["device"] == "FungalFrequencies_7483aff9d108")"""

queryF = """from(bucket: "fungalF")
    |> range(start: {time}s)
    |> filter(fn: (r) => r["_measurement"] == "adcData")
    |> filter(fn: (r) => r["ADC"] == "ADS1115")
    |> filter(fn: (r) => r["_field"] == "CH_0" or r["_field"] == "CH_1" or r["_field"] == "CH_3" or r["_field"] == "CH_2" or r["_field"] == "CH_4" or r["_field"] == "CH_5" or r["_field"] == "CH_6" or r["_field"] == "CH_7")
    |> filter(fn: (r) => r["board"] == "{board}")
    |> filter(fn: (r) => r["device"] == "{device}")"""

queryFS = """from(bucket: "fungalF")
    |> range(start: {time}s)
    |> filter(fn: (r) => r["_measurement"] == "adcData")
    |> filter(fn: (r) => r["ADC"] == "ADS1115")
    |> filter(fn: (r) => r["_field"] == "CH_0" or r["_field"] == "CH_1" or r["_field"] == "CH_3" or r["_field"] == "CH_2" or r["_field"] == "CH_4" or r["_field"] == "CH_5" or r["_field"] == "CH_6" or r["_field"] == "CH_7")
    |> filter(fn: (r) => r["board"] == "{board}")
    |> filter(fn: (r) => r["device"] == "{device}")
    |> aggregateWindow(every: {step}s, fn: mean, createEmpty: true)"""


# print(fetchData(query3))