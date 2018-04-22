from globals.layer_globals import *
from globals import topology_globals
import traceback
import datetime
import math


def app_layer_forward(inst, msg):
    msg = eval(msg)
    print 'Message received from (%s, %s).\tContent: %s' % (msg['host'], msg['port'], msg['message'])


def app_layer_operation(inst, msg):
    msg = eval(msg)
    print 'Message received from (%s, %s).\nContent: %s' % (msg['host'], msg['port'], msg['message'])
    msg['port'] -= 12
    msg['action_type'] = SEND_TO_LOWER
    inst.send_packet(str(msg), msg['action_type'])


def network_layer_operation(inst, msg):
    print 'Arrived network layer with: ' + msg
    msg = eval(msg)
    if msg['action_type'] not in (SEND_TO_UPPER, SEND_TO_LOWER, NETWORK_BROADCAST):
        print 'Erroneous action!'
        return False
    try:
        if msg['action_type'] == SEND_TO_UPPER:
            if 'is_broadcast' not in msg:
                inst.send_packet(msg, msg['action_type'])
            else:
                # TODO: Update routing table.
                pass
        elif msg['action_type'] == SEND_TO_LOWER:
            # TODO: Routing.
            msg['port'] += 10012
            inst.send_packet(msg, msg['action_type'])

    except:
        print 'Error occurred in network layer.'
        return False
    return True


def phy_link_layer_operation(inst, msg):
    print 'Arrived phy_link layer with: ' + msg
    msg = eval(msg)
    if msg['action_type'] not in [SEND_TO_UPPER, SEND_TO_LOWER, NETWORK_BROADCAST]:
        print 'Erroneous action!'
        return False

    distance = math.sqrt(math.pow(inst._x - msg['source_x'], 2) + math.pow(inst._y - msg['source_y'], 2))
    if distance > topology_globals.WIRELESS_RANGE:
        return False

    try:
        if msg['action_type'] == SEND_TO_UPPER:
            msg['recv_date'] = datetime.datetime.utcnow()
            inst.send_packet(msg, msg['action_type'])
        elif msg['action_type'] in [SEND_TO_LOWER]:
            msg['action_type'] = SEND_TO_UPPER
            msg['send_date'] = datetime.datetime.utcnow()
            inst.send_to_channel(msg)

    except:
        traceback.print_exc()
        print 'Error occurred in phy_link layer.'
        return False
    return True
