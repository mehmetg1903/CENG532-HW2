import traceback
import zmq
from globals.layer_globals import *

class LayerElement(object):
    def __init__(self, rcv_ports=(-1,-1), snd_ports=(-1,-1), to_int='localhost'):
        self._port_recv_from_lower = rcv_ports[0]
        self._port_recv_from_upper = rcv_ports[1]
        self._port_send_to_lower = snd_ports[0]
        self._port_send_to_upper = snd_ports[1]
        self._context = zmq.Context()


        if self._port_recv_from_lower != -1:
            self._sock_recv_from_lower = self._context.socket(zmq.PULL)
            self._sock_recv_from_lower.bind('tcp://*:%s' % str(self._port_recv_from_lower))

        if self._port_recv_from_upper != -1:
            self._sock_recv_from_upper = self._context.socket(zmq.PULL)
            self._sock_recv_from_upper.bind('tcp://*:%s' % str(self._port_recv_from_upper))

        if self._port_send_to_lower != -1:
            self._sock_send_to_lower = self._context.socket(zmq.PUSH)
            self._sock_send_to_lower.bind('tcp://%s:%s' % (to_int, str(self._port_send_to_lower)))

        if self._port_send_to_upper != -1:
            self._sock_send_to_upper = self._context.socket(zmq.PUSH)
            self._sock_send_to_upper.bind('tcp://%s:%s' % (to_int, str(self._port_send_to_upper)))

    @classmethod
    def send_packet(json_packet, to_interface):
        if to_interface not in [SEND_TO_UPPER, SEND_TO_LOWER]:
            raise Exception('Unknown operation. please pick one of them: (%s, %s)' % (str(SEND_TO_UPPER), str(SEND_TO_CHANNEL)))

        try:
            if not hasattr(self, _sock_send_to_upper):
                raise Exception()
            if not hasattr(self, _sock_send_to_lower):
                raise Exception()

            if to_interface == SEND_TO_UPPER:
                self._sock_send_to_upper.send_json(json_packet)
            else:
                self._sock_send_to_lower.send_json(json_packet)
        except:
            traceback.print_exc()
            return False
        return True

    @classmethod
    def start_listenning(from_interface, basic_operation):
        if from_interface not in [RECV_FROM_UPPER, RECV_FROM_LOWER]:
            raise Exception('Unknown operation. please pick one of them: (%s, %s)' % (str(RECV_FROM_UPPER), str(RECV_FROM_LOWER)))

        try:
            if to_interface == SEND_TO_UPPER:
                if not hasattr(self, _sock_recv_from_upper):
                    raise Exception()
                while True:
                    row_msg = self._sock_recv_from_upper.recv_json()
                    basic_operation(row_msg)
            else:
                if not hasattr(self, _sock_recv_from_lower):
                    raise Exception()
                while True:
                    row_msg = self._sock_recv_from_lower.recv_json()
                    basic_operation(row_msg)
        except:
            traceback.print_exc()
            return False
