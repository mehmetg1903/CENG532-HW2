from mininet.util import dumpNodeConnections
from mininet.net import Mininet
from mininet.topo import Topo


from sys import argv


class CEng532Topology(Topo):
    def __init__(self, _loss=10, _hc=5, **kwargs):
        Topo.__init__(self, **kwargs)

        hosts = dict()
        hosts['swc'] = self.addHost('swc')
        swc = self.addSwitch('s1')
        self.addLink(swc, hosts['swc'])
        for i in range(1, _hc + 1):
            hosts['h' + str(i)] = self.addHost('h' + str(i), delay=100)
            self.addLink(swc, hosts['h' + str(i)])


topos = {
    'hw1_topo': (lambda: CEng532Topology())
}