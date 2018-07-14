#!/usr/bin/env python

from elasticsearch import Elasticsearch
from datetime import datetime
from dateutil import parser
import requests
import pytz
from dateutil import tz

es = Elasticsearch([{'host': 'nuccie.local', 'port': 9200}])

res = es.search(index="zonnepanelen", body={"query": {"match_all": {}}, "size": 20, "sort": [
    {
      "timestamp": {
        "order": "desc"
      }
    }
  ]})


body = {}
body["c1"]=1
body["data"]=""
from_timezone   = tz.gettz('UTC')
to_timezone     = tz.gettz('Europe/Brussels')

for doc in res['hits']['hits']:

    source = doc['_source']
    timestamp   = parser.parse(source['timestamp'])
    timestamp   = timestamp.replace(tzinfo=from_timezone)
    timestamp   = timestamp.astimezone(to_timezone)

    date        = timestamp.strftime("%Y%m%d")
    hour        = timestamp.strftime("%H:%M")
    watthours   = source['WattHours']
    power       = source['Watts']
    temperature = source['Heat Sink Temperature']
    voltage     = source['DC Voltage']
    measurement = "%s,%s,%s,%s,0,0,%s,%s" % (date, hour, watthours, power, temperature, voltage)
    body["data"] = body["data"] + measurement + ";"



headers = {
    'X-Pvoutput-Apikey':'653005284e51f7e0749e8d2f98b9c42c5d09ffae',
    'X-Pvoutput-SystemId':'60441'
}

r = requests.post('https://pvoutput.org/service/r2/addbatchstatus.jsp', data = body, headers=headers)
print(r.status_code)
