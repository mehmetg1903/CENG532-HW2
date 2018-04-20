from layer_element import LayerElement

def basic_operation(row_msg):
    print row_msg

if __name__ == "__main__":
    elem1 = LayerElement((11000, 11005), (21000, 21005), '127.0.0.1')
    elem2 = LayerElement((21000, 21005), (11000, 11005), '127.0.0.1')
    elem1.start_listenning(3, basic_operation)
    row_msg = {'msg' : 'Hello World!'}
    elem2.send_packet(2, row_msg)
