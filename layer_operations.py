from globals.layer_globals import *
import traceback
import zmq

def app_layer_forward(inst, msg):
    msg = eval(msg)
    print 'Message received from (%s, %s).\nContent: %s' % (msg['host'], msg['port'], msg['message'])

def app_layer_operation(inst, msg):
    msg = eval(msg)
    print 'Message received from (%s, %s).\nContent: %s' % (msg['host'], msg['port'], msg['message'])
    msg['port'] -= 12
    msg['action_type'] = SEND_TO_LOWER
    inst.send_packet(str(msg), SEND_TO_LOWER)


def network_layer_operation(inst, msg):
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
    msg = eval(msg)
    if msg['action_type'] not in [SEND_TO_UPPER, SEND_TO_LOWER, NETWORK_BROADCAST]:
        print 'Erroneous action!'
        return False
    try:
        if msg['action_type'] == SEND_TO_UPPER:
            inst.send_packet(msg, msg['action_type'])
        elif msg['action_type'] in [SEND_TO_LOWER]:
            msg['action_type'] = SEND_TO_UPPER
            inst.send_to_channel(msg)

    except:
        traceback.print_exc()
        print 'Error occurred in phy_link layer.'
        return False
    return True
