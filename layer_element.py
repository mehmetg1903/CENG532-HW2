import traceback
import threading
import zmq
import uuid
import pickle
from globals.layer_globals import *
from globals import topology_globals

class LayerElement(object):
    def __init__(self, _port_recv_from_lower=-1, _port_recv_from_upper=-1, _port_send_to_lower=-1, _port_send_to_upper=-1, _x=0, _y=0, to_int='127.0.0.1'):
        self._channel_connections = dict()
        self._x = _x
        self._y = _y
        self.active_route_requests = set()

        if _port_recv_from_lower != -1:
            self._context_recv_from_lower = zmq.Context()
            # print '_sock_recv_from_lower: %s OK!' % str(_port_recv_from_lower)
            self._sock_recv_from_lower = self._context_recv_from_lower.socket(zmq.PAIR)
            self._sock_recv_from_lower.bind('tcp://%s:%s' % (to_int, str(_port_recv_from_lower)))

        if _port_recv_from_upper != -1:
            self._context_recv_from_upper = zmq.Context()
            # print '_sock_recv_from_upper: %s OK!' % str(_port_recv_from_upper)
            self._sock_recv_from_upper = self._context_recv_from_upper.socket(zmq.PAIR)
            self._sock_recv_from_upper.bind('tcp://%s:%s' % (to_int, str(_port_recv_from_upper)))

        if _port_send_to_lower != -1:
            self._context_send_to_lower = zmq.Context()
            # print '_sock_send_to_lower: %s OK!' % str(_port_send_to_lower)
            self._sock_send_to_lower = self._context_send_to_lower.socket(zmq.PAIR)
            self._sock_send_to_lower.connect('tcp://%s:%s' % (to_int, str(_port_send_to_lower)))

        if _port_send_to_upper != -1:
            self._context_send_to_upper = zmq.Context()
            # print '_sock_send_to_upper: %s OK!' % str(_port_send_to_upper)
            self._sock_send_to_upper = self._context_send_to_upper.socket(zmq.PAIR)
            self._sock_send_to_upper.connect('tcp://%s:%s' % (to_int, str(_port_send_to_upper)))

    def send_packet(self, json_packet, to_interface):
        if to_interface not in [SEND_TO_UPPER, SEND_TO_LOWER]:
            raise Exception('Unknown operation. please pick one of them: (%s, %s)' % (str(SEND_TO_UPPER), str(SEND_TO_LOWER)))

        try:
            if to_interface == SEND_TO_UPPER:
                self._sock_send_to_upper.send(str(json_packet))
            elif to_interface == SEND_TO_LOWER:
                self._sock_send_to_lower.send(str(json_packet))
        except:
            traceback.print_exc()
            return False
        return True

    def send_to_channel(self, json_packet):
        if len(self._channel_connections.keys()) == 0:
            self._channel_context = zmq.Context()

        try:
            HOST, PORT = json_packet['host'], json_packet['port']
            print HOST, PORT
            if HOST not in self._channel_connections:
                self._channel_connections[HOST] = self._channel_context.socket(zmq.PAIR)
                self._channel_connections[HOST].connect('tcp://%s:%s' % (HOST, str(PORT)))

            sock = self._channel_connections[HOST]
            sock.send(str(json_packet))
        except:
            traceback.print_exc()
            return False
        return True

    def create_rreq_package(self, dest):
        rreq_package = {
            'id': uuid.uuid4().int,
            'source': self.ip, #TODO,
            'destination': dest, #TODO,
            'route': list()
        }

    def route_request(self, rreq_packet=None, dest=None):
        if rreq_packet == None: # Source node
            rreq_packet = self.create_rreq_package(dest)
            self.active_route_requests.add(rreq_packet['id'])
        else: # Junction or destination node
            if rreq_packet['id'] in self.active_route_requests:
                return
            else:
                if rreq_packet['dest'] == self.ip:
                    route_response(rreq_packet)
                    return
                else:
                    rreq_packet['route'].append(self.ip)
                    self.active_route_requests.add(rreq_packet['id'])

        for node in topology_globals.nodes:
            json_packet = {
                'host': self.ip,
                'source_x': self._x,
                'source_y': self._y,
                'message_type': topology_globals.RREQ,
                'rreq_packet': rreq_packet
            }
            self.send_packet(json_packet, SEND_TO_LOWER)


    def start_listenning(self, basic_operation, listen_interfaces):
        threads = []
        for listen_interface in listen_interfaces:
            t = threading.Thread(target=listen_interface_worker, args=(self, basic_operation, listen_interface))
            threads.append(t)
            t.start()

def listen_interface_worker(self, basic_operation, listen_interface):
    if listen_interface not in [RECV_FROM_LOWER, RECV_FROM_UPPER]:
        return 0
    if listen_interface == RECV_FROM_LOWER:
        while True:
            row_msg = self._sock_recv_from_lower.recv(1024)
            basic_operation(self, row_msg)
    elif listen_interface == RECV_FROM_UPPER:
        while True:
            row_msg = self._sock_recv_from_upper.recv(1024)
            basic_operation(self, row_msg)
