from layer_element import LayerElement

def basic_operation(row_msg):
    print row_msg

if __name__ == "__main__":
    elem4 = LayerElement(_port_recv_from_lower=50013, _port_send_to_lower=50008, to_int='127.0.0.1')
    elem4.start_listenning(basic_operation, [4])
