from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.topo import SingleSwitchTopo
from mininet.link import TCLink

from sys import argv

class CEng532Topology( Topo ):

    def __init__( self, _loss=10, _hc=5, **kwargs ):
        Topo.__init__( self, **kwargs )

        hosts = dict()
        hosts['switch'] = self.addHost( 'switch' )
        swc = self.addSwitch('s1')
        self.addLink(swc, hosts['switch'])
        for i in range( 1, _hc + 1 ):
            hosts['h' + str(i)] = self.addHost( 'h' + str(i) )
            self.addLink(swc, hosts['h' + str(i)])
            # self.addLink( hosts['switch'], hosts['h' + str(i)])


if __name__ == "__main__":
    if len(argv) > 1:
        hc = int(argv[1])
    else:
        hc = 5
    topo = CEng532Topology(_hc=hc)
    net = Mininet(topo)
    net.start()
    dumpNodeConnections(net.hosts)
    # execfile("confme.py")
    for h in net.hosts:

        print h.name, ' - ', h.IP

    net.stop()
