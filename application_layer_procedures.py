from globals.layer_globals import *
from globals import topology_globals
import traceback
import datetime
import time


def broadcast_nodes_in_range(inst):
    while True:
        msg = dict()
        msg['message_type'] = NETWORK_BROADCAST
        msg['action_type'] = SEND_TO_LOWER
        msg['host'] = inst.ip
        msg['nodes'] = inst.nodes_in_range

        inst.send_packet(str(msg), msg['action_type'])
        time.sleep(topology_globals.TIMEOUT)


def get_priority_of_host(ip):
    try:
        return int(ip[ip.rfind('.') + 1:])
    except:
        return -1


def handle_leader_election(inst):
    while True:

        if inst.leader is  None:
            inst.leader = inst.ip
            msg = dict()
            inst.broadcast_election(msg)
        else:
            if get_priority_of_host(inst.ip) > get_priority_of_host(inst.leader):
                inst.leader = inst.ip
                msg = dict()
                inst.broadcast_election(msg)
        time.sleep(topology_globals.TIMEOUT)


def detect_network(inst, msg):
    eval(msg)
    inst.nodes_in_range.union(msg['nodes'])
