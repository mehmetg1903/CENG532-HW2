from layer_element import LayerElement

def basic_operation(row_msg):
    print row_msg

if __name__ == "__main__":
    elem1 = LayerElement(_port_recv_from_lower=40013, _port_send_to_lower=40008, to_int='127.0.0.1')
    elem1.start_listenning(basic_operation, [4])
