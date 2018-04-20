from layer_operations import *
from layer_element import LayerElement
from globals.layer_globals import *

if __name__ == "__main__":
    app_elem = LayerElement(_port_recv_from_lower=40010, _port_send_to_lower=40000)
    app_elem.start_listenning(app_layer_operation, [RECV_FROM_LOWER])
    # TODO: Add send operations
    network_elem = LayerElement(_port_recv_from_lower=40011, _port_send_to_lower=40001,
                                _port_recv_from_upper=40000, _port_send_to_upper=40010)
    network_elem.start_listenning(network_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
    phy_link_elem = LayerElement(_port_recv_from_lower=40012, _port_recv_from_upper=40001, _port_send_to_upper=40011)
    phy_link_elem.start_listenning(phy_link_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
