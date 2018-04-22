#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI

class homework2Topology( Topo ):

    def __init__( self, _loss=10, **kwargs ):
        Topo.__init__( self, **kwargs )
        maxq = 800
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        s0 = self.addHost( 's0' )
        s1 = self.addHost( 's1' )
        s2 = self.addHost( 's2' )
        s3 = self.addHost( 's3' )

	self.addLink( h1, s0, bw=100, delay='1ms', loss= 1, max_queue_size= maxq  )
	self.addLink( s0, s1, bw=10, delay='5ms', loss= _loss, max_queue_size= maxq  )
	self.addLink( s1, h2, bw=100, delay='1ms', loss=1, max_queue_size= maxq  )

	self.addLink( h1, s2, bw=100, delay='1ms', loss=1, max_queue_size= maxq  )
	self.addLink( s2, s3, bw=10, delay='5ms', loss= _loss, max_queue_size= maxq  )
	self.addLink( s3, h2, bw=100, delay='1ms', loss=1, max_queue_size= maxq  )

#topos = { 'homework2Topology': ( lambda **args: homework2Topology(**args) ) }

def func(loss):
	topo = homework2Topology()
	net = Mininet(topo,loss, link=TCLink)
	net.start()
	execfile("confme.py")
	net.stop()
	print "Values for loss: ", loss, " are following:"
	h1 = net.get('h1')
	h2 = net.get('h2')
	h1.cmd('python server_UDPO.py &')
	result = h2.cmd("python client_UDPO.py")
	print result
if __name__ == '__main__':
	for i in range(1,6):
		func(i)
