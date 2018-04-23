from layer_operations import *
from layer_element import LayerElement
from globals.layer_globals import *
import random
from sys import argv


def simulate(send_port=10000, recv_port=10012, max_dist=150):
    app_elem = LayerElement(_port_recv_from_lower=recv_port, _port_send_to_lower=send_port)
    app_elem.start_listenning(app_layer_forward, [RECV_FROM_LOWER])
    network_elem = LayerElement(_port_recv_from_lower=recv_port, _port_send_to_lower=send_port + 1,
                                _port_recv_from_upper=send_port, _port_send_to_upper=recv_port)
    network_elem.start_listenning(network_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
    x = random.random() % max_dist
    y = random.random() % max_dist
    phy_link_elem = LayerElement(_port_recv_from_lower=recv_port, _port_recv_from_upper=send_port + 1,
                                 _port_send_to_upper=recv_port, _x=x, _y=y)
    phy_link_elem.start_listenning(phy_link_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
    msg = {}
    msg['action_type'] = SEND_TO_LOWER
    msg['dest'] = '10.0.0.%s' % (random.random() % 5 + 1)
    msg['message_type'] = topology_globals.FRAME
    app_elem.send_packet(str(msg), msg['action_type'])


if __name__ == '__main__':
    if len(argv) > 1:
        max_dist = int(argv[1])
    else:
        max_dist = 150
    simulate()
