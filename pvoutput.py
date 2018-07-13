#!/usr/bin/env python

import sunspec.core.client as client
import sunspec.core.suns as suns
import requests
from datetime import datetime

headers = {
    'X-Pvoutput-Apikey':'653005284e51f7e0749e8d2f98b9c42c5d09ffae',
    'X-Pvoutput-SystemId':'60441'
}

try:
    sd = client.SunSpecClientDevice(client.TCP, 1, ipaddr="192.168.0.158", ipport=502, timeout=2.0)
except client.SunSpecClientError, e:
    print('Error: %s' % (e))
    sys.exit(1)

data = {}

if sd is not None:
    sd.read()

    for model in sd.device.models_list:
        for block in model.blocks:
            for point in block.points_list:
                if point.value is not None:
                    if point.point_type.id == "WH":
                        data["v1"] = point.value
                    if point.point_type.id == "W":
                        data["v2"] = point.value


if len(data) is not 0:
    data['d']=datetime.now().strftime("%Y%m%d")
    data['t']=datetime.now().strftime("%H:%M")
    data['c1']=1 #culumatieve waarde!
    r = requests.post('https://pvoutput.org/service/r2/addstatus.jsp', data = data, headers=headers)
    print(r.text)
else:
    print("No Data")
