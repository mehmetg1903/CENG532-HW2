from layer_operations import *
from layer_element import LayerElement
from globals.layer_globals import *


def simulate(send_port=10000, recv_port=10012, max_node=5):
    app_elem = LayerElement(_port_recv_from_lower=recv_port, _port_send_to_lower=send_port)
    app_elem.start_listenning(app_layer_forward, [RECV_FROM_LOWER])
    network_elem = LayerElement(_port_recv_from_lower=recv_port, _port_send_to_lower=send_port+1,
                                _port_recv_from_upper=send_port, _port_send_to_upper=recv_port)
    network_elem.start_listenning(network_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
    phy_link_elem = LayerElement(_port_recv_from_lower=recv_port, _port_recv_from_upper=send_port+1, _port_send_to_upper=recv_port)
    phy_link_elem.start_listenning(phy_link_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])




