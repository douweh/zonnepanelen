#!/usr/bin/env python

import sunspec.core.client as client
import sunspec.core.suns as suns

try:
    sd = client.SunSpecClientDevice(client.TCP, 1, ipaddr="192.168.0.158", ipport=502, timeout=2.0)
except client.SunSpecClientError, e:
    print('Error: %s' % (e))
    sys.exit(1)

if sd is not None:
    sd.read()

    for model in sd.device.models_list:
        if model.model_type.label:
            label = '%s (%s)' % (model.model_type.label, str(model.id))
        else:
            label = '(%s)' % (str(model.id))
        print('\nmodel: %s\n' % (label))
        for block in model.blocks:
            if block.index > 0:
              index = '%02d:' % (block.index)
            else:
              index = '   '
            for point in block.points_list:
                if point.value is not None:
                    if point.point_type.label:
                        label = '   %s%s (%s):' % (index, point.point_type.label, point.point_type.id)
                    else:
                        label = '   %s(%s):' % (index, point.point_type.id)
                    units = point.point_type.units
                    if units is None:
                        units = ''
                    if point.point_type.type == suns.SUNS_TYPE_BITFIELD16:
                        value = '0x%04x' % (point.value)
                    elif point.point_type.type == suns.SUNS_TYPE_BITFIELD32:
                        value = '0x%08x' % (point.value)
                    else:
                        value = str(point.value).rstrip('\0')
                    print('%-40s %20s %-10s' % (label, value, str(units)))
