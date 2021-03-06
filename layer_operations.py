from globals.layer_globals import *
from globals import topology_globals
import traceback
import datetime
import math
import application_layer_procedures


def switch_app_operation(inst, msg):
    msg = eval(msg)
    if msg['action_type'] == SEND_TO_UPPER:
        if msg["message_type"] == topology_globals.ELECTION_LEADER_ANNOUNCE:
            inst.leader = msg["src_ip"]
            if inst.algorithm == 'modified':
                inst.prepare_grant(inst.leader)
            for node in [e for e in inst.nodes_in_range if e != inst.ip]:
                msg['action_type'] = SEND_TO_LOWER
                msg["dest"] = node
                inst.send_packet(msg, SEND_TO_LOWER)

        elif msg["message_type"] == topology_globals.ELECTION_LEADER_GRANT:
            pass


def app_layer_forward(inst, msg):
    msg = eval(msg)
    print 'Message received from (%s, %s).\tContent: %s' % (msg['host'], msg['port'], msg['message'])

    if msg['action_type'] == SEND_TO_UPPER:
        if msg['message_type'] == NETWORK_BROADCAST:
            application_layer_procedures.detect_network(inst)


def app_layer_operation(inst, msg):
    msg = eval(msg)
    print 'Message received from (%s, %s).\nContent: %s' % (msg['host'], msg['port'], msg['message'])
    msg['action_type'] = SEND_TO_LOWER
    msg['dest'] = '10.0.0.3'
    msg['message_type'] = topology_globals.FRAME
    inst.send_packet(str(msg), msg['action_type'])


def switch_network_operation(inst, msg):
    msg = eval(msg)
    if msg['action_type'] not in (SEND_TO_UPPER, SEND_TO_LOWER, NETWORK_BROADCAST):
        print 'Erroneous action!'
        return False
    inst.send_packet(msg, msg['action_type'])


def network_layer_operation(inst, msg):
    print 'Arrived network layer with: ' + msg
    msg = eval(msg)
    if msg['action_type'] not in (SEND_TO_UPPER, SEND_TO_LOWER, NETWORK_BROADCAST):
        print 'Erroneous action!'
        return False
    try:
        if msg['action_type'] == SEND_TO_UPPER:
            if msg['message_type'] == topology_globals.RREQ:
                msg['action_type'] = SEND_TO_LOWER
                msg = inst.route_request(msg)
                inst.send_packet(msg, msg['action_type'])

            elif msg['message_type'] == topology_globals.RRESP:
                if msg['rreq_package']['source'] != inst.ip:
                    msg['action_type'] = SEND_TO_LOWER
                    msg = inst.route_response(msg)
                    inst.send_packet(msg, msg['action_type'])
                else:
                    inst.active_route_requests.pop(msg['rreq_package']['id'])
                    rreq_package_tmp = msg['rreq_package']
                    msg = inst.route_requiring_message.pop(rreq_package_tmp['id'])
                    msg['rreq_package'] = rreq_package_tmp
                    msg['dest'] = msg['rreq_package']['route'][0]
                    msg['message_type'] = topology_globals.FRAME
                    msg['action_type'] = SEND_TO_LOWER
                    inst.send_packet(msg, msg['action_type'])

            elif msg['message_type'] == topology_globals.FRAME:
                if msg['rreq_package']['dest'] == inst.ip:
                    msg['action_type'] = SEND_TO_UPPER
                    inst.send_packet(msg, msg['action_type'])
                else:
                    msg['dest'] = msg['rreq_package']['route'][msg['rreq_package']['route'].index(inst.ip) + 1]
                    msg['action_type'] = SEND_TO_LOWER
                    inst.send_packet(msg, msg['action_type'])

            elif msg['message_type'] == NETWORK_BROADCAST:
                inst.send_packet(msg, msg['action_type'])


        elif msg['action_type'] == SEND_TO_LOWER:
            if msg['message_type'] == topology_globals.RREQ:
                msg = inst.route_request(msg)
                inst.send_packet(msg, msg['action_type'])

            elif msg['message_type'] == topology_globals.FRAME:
                msg_tmp = msg
                msg = inst.route_request(msg)
                inst.route_requiring_message[msg['rreq_package']['id']] = msg_tmp
                inst.send_packet(msg, msg['action_type'])

            elif msg['message_type'] == NETWORK_BROADCAST:
                inst.send_packet(msg, msg['action_type'])

            elif msg['message_type'] == topology_globals.ELECTION_LEADER_ANNOUNCE:
                inst.send_packet(msg, msg['action_type'])

        return True

    except:
        print traceback.format_exc()
        print 'Error occurred in network layer.'
        return False


def phy_link_layer_operation(inst, msg):
    print 'Arrived phy_link layer with: ' + msg
    msg = eval(msg)
    if msg['action_type'] not in [SEND_TO_UPPER, SEND_TO_LOWER, NETWORK_BROADCAST]:
        print 'Erroneous action!'
        return False

    try:
        if msg['action_type'] == SEND_TO_UPPER:
            # Simulate wireless communication range
            distance = math.sqrt(math.pow(inst._x - msg['source_x'], 2) + math.pow(inst._y - msg['source_y'], 2))
            if distance > topology_globals.WIRELESS_RANGE:
                return False

            if 'is_broadcast' in msg.keys():
                if msg['is_broadcast'] == 1:
                    inst.broadcast(msg)

            msg['recv_date'] = datetime.datetime.utcnow()
            inst.send_packet(msg, msg['action_type'])

        elif msg['action_type'] in [SEND_TO_LOWER]:
            msg['action_type'] = SEND_TO_UPPER
            msg['source_x'] = inst._x
            msg['source_y'] = inst._y
            msg['send_date'] = datetime.datetime.utcnow()
            inst.send_to_channel(msg)

        return True

    except:
        print 'Error occurred in phy_link layer.'
        return False
