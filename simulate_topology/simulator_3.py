from layer_operations import *
from layer_element import LayerElement
from globals.layer_globals import *

if __name__ == "__main__":
    app_elem = LayerElement(_port_recv_from_lower=30010, _port_send_to_lower=30000)
    app_elem.start_listenning(app_layer_operation, [RECV_FROM_LOWER])
    # TODO: Add send operations
    network_elem = LayerElement(_port_recv_from_lower=30011, _port_send_to_lower=30001,
                                _port_recv_from_upper=30000, _port_send_to_upper=30010)
    network_elem.start_listenning(network_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
    phy_link_elem = LayerElement(_port_recv_from_lower=30012, _port_recv_from_upper=30001, _port_send_to_upper=30011)
    phy_link_elem.start_listenning(phy_link_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
