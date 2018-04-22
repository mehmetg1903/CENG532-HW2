from layer_operations import *
from layer_element import LayerElement
from globals.layer_globals import *

if __name__ == "__main__":
    app_elem = LayerElement(_port_recv_from_lower=50010, _port_send_to_lower=50000)
    app_elem.start_listenning(app_layer_operation, [RECV_FROM_LOWER])
    # TODO: Add send operations
    network_elem = LayerElement(_port_recv_from_lower=50011, _port_send_to_lower=50001,\
                                       _port_recv_from_upper=50000, _port_send_to_upper=50010)
    network_elem.start_listenning(network_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
    phy_link_elem = LayerElement(_port_recv_from_lower=50012, _port_recv_from_upper=50001, _port_send_to_upper=50011)
    phy_link_elem.start_listenning(phy_link_layer_operation, [RECV_FROM_LOWER, RECV_FROM_UPPER])
