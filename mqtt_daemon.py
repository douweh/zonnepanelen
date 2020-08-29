import paho.mqtt.client as mqtt
import time, threading, ssl, random
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch([{'host': 'nuccie.local', 'port': 9200}])

# client, user and device details
serverUrl   = "nuccie.local"
clientId    = "my_mqtt_python_daemon"

receivedMessages = []

# display all incoming messages
def on_message(client, userdata, message):
    data = {}
    data['timestamp']=datetime.utcnow()
    if (b"puls" in message.payload):
        if b"pv_puls" in message.payload:
            data['pv']=1
        if b"consumption_puls" in message.payload:
            data['consumption']=1
        if b"gas_puls" in message.payload:
            data['gas']=1
        es.index(index='gasmeter', doc_type='logs', body=data)
        print(data)

client = mqtt.Client(clientId)
client.on_message = on_message
client.connect(serverUrl)

print("Device registered successfully!")

client.subscribe("metersensor")

client.loop_forever()  # Start networking daemon
