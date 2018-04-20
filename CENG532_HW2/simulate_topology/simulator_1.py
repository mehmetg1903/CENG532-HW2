import pickle
from layer_operations import *
from layer_element import LayerElement
from globals.layer_globals import *


if __name__ == "__main__":
    app_elem = LayerElement(_port_recv_from_lower=10010, _port_send_to_lower=10000)
    app_elem.start_listenning(app_layer_forward, [RECV_FROM_LOWER])
    network_elem = LayerElement(_port_recv_from_lower=10011, _port_send_to_lower=10001,\
                                       _port_recv_from_upper=10000, _port_send_to_upper=10010)
    network_elem.start_listenning(network_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
    phy_link_elem = LayerElement(_port_recv_from_lower=10012, _port_recv_from_upper=10001, _port_send_to_upper=10011)
    phy_link_elem.start_listenning(phy_link_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
    msg = dict()
    msg['host'] = '127.0.0.1'
    msg['port'] = 10000
    msg['message'] = 'Loves from machine.'
    msg['action_type']  = SEND_TO_LOWER
    print msg
    app_elem.send_packet(str(msg), SEND_TO_LOWER)
