#!/usr/bin/env python

import requests, json
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch([{'host': 'nuccie.local', 'port': 9200}])

data = {}

url = "http://metersensor.local/reset"
r = requests.post(url, json={"key": "value"})

if r.status_code == 200:
  data = r.json()
  print("Adding data to elasticsearch")
  data['timestamp']=datetime.utcnow()
  es.index(index='gasmeter', doc_type='logs', body=data)
  print data
