from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink

from sys import argv

class homework2Topology( Topo ):

    def __init__( self, _loss=10, _hc=5, **kwargs ):
        Topo.__init__( self, **kwargs )
        maxq = 800

        hosts = dict()
        hosts['switch'] = self.addHost( 'switch' )
        for i in range( 1, _hc + 1 ):
            hosts['h' + str(i)] = self.addHost( 'h' + str(i) )
            self.addLink( hosts['switch'], hosts['h' + str(i)], bw=100, delay='1ms', loss= 1, max_queue_size= maxq  )

if __name__ == "__main__":
    if len(argv) > 1:
        hc = int(argv[1])
    else:
        hc = 5
    net = Mininet(topo,loss, link=TCLink)
	net.start()
	execfile("confme.py")
	net.stop()
