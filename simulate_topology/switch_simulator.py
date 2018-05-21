from layer_operations import *
from layer_element import LayerElement
from globals.layer_globals import *
import random
from sys import argv
import socket

from threading import Thread
import application_layer_procedures


def simulate(algo='bully'):
    send_port = 10000
    recv_port = 10012
    max_dist = 150
    ip = socket.gethostbyname(socket.gethostname())
    app_elem = LayerElement(_port_recv_from_lower=recv_port - 2, _port_send_to_lower=send_port, ip=ip, algorithm=algo)
    app_elem.start_listenning(switch_app_operation, [RECV_FROM_LOWER])
    network_elem = LayerElement(_port_recv_from_lower=recv_port - 1, _port_send_to_lower=send_port + 1,
                                _port_recv_from_upper=send_port, _port_send_to_upper=recv_port - 2, ip=ip,
                                algorithm=algo)
    network_elem.start_listenning(switch_network_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
    x = random.random() % max_dist
    y = random.random() % max_dist
    phy_link_elem = LayerElement(_port_recv_from_lower=recv_port, _port_recv_from_upper=send_port + 1,
                                 _port_send_to_upper=recv_port - 1, _x=x, _y=y, ip=ip, algorithm=algo)
    phy_link_elem.start_listenning(phy_link_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])

    threads = []

    node_list_bcast_thread = Thread(target=application_layer_procedures.broadcast_nodes_in_range, args=(app_elem,))
    node_list_bcast_thread.start()
    threads.append(node_list_bcast_thread)

    leader_election_thread = Thread(target=application_layer_procedures.handle_leader_election, args=(app_elem,))
    leader_election_thread.start()
    threads.append(leader_election_thread)

    for t in threads:
        t.join()


if __name__ == '__main__':
    if len(argv) > 1:
        algorithm = int(argv[1])
    else:
        algorithm = 0
    simulate(algo='bully' if algorithm == 0 else 'modified')
