import json
from layer_element import LayerElement

def basic_operation(row_msg):
    print row_msg

if __name__ == "__main__":
    elem3 = LayerElement(_port_recv_from_upper=40008, _port_send_to_upper=40013, to_int='127.0.0.1')
    row_msg = {'msg' : 'Hello World from elem3_40000!'}
    elem3.send_packet(json.dumps(row_msg), 1)
    elem3_2 = LayerElement(_port_recv_from_upper=50008, _port_send_to_upper=50013, to_int='127.0.0.1')
    row_msg = {'msg' : 'Hello World from elem3_50000!'}
    elem3_2.send_packet(json.dumps(row_msg), 1)
