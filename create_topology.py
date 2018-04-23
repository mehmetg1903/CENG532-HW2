from mininet.util import dumpNodeConnections
from mininet.net import Mininet
from mininet.topo import Topo

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

topos = {
    'hw1_topo' : ( lambda : CEng532Topology())
}


def monitorFiles( outfiles, seconds, timeoutms ):
    devnull = open( '/dev/null', 'w' )
    tails, fdToFile, fdToHost = {}, {}, {}
    for h, outfile in outfiles.iteritems():
        tail = Popen( [ 'tail', '-f', outfile ],
                      stdout=PIPE, stderr=devnull )
        fd = tail.stdout.fileno()
        tails[ h ] = tail
        fdToFile[ fd ] = tail.stdout
        fdToHost[ fd ] = h
    # Prepare to poll output files
    readable = poll()
    for t in tails.values():
        readable.register( t.stdout.fileno(), POLLIN )
    # Run until a set number of seconds have elapsed
    endTime = time() + seconds
    while time() < endTime:
        fdlist = readable.poll(timeoutms)
        if fdlist:
            for fd, _flags in fdlist:
                f = fdToFile[ fd ]
                host = fdToHost[ fd ]
                # Wait for a line of output
                line = f.readline().strip()
                yield host, line
        else:
            # If we timed out, return nothing
            yield None, ''
    for t in tails.values():
        t.terminate()
    devnull.close()  # Not really necessary


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
    outfiles = {}
    errfiles = {}
    for h in net.hosts:
        print h.name, ' - ', h.IP
        outfiles[h] = '/tmp/%s.out' % h.name
        errfiles[h] = '/tmp/%s.out' % h.name
        h.cmd( 'echo >', outfiles[ h ] )
        h.cmd( 'echo >', errfiles[ h ] )
        h.cmdPrint('python -m simulate_topology.main_simulator'
                   '>', outfiles[h],
                   '2>', errfiles[h],
                   '&')
    for h, line in monitorFiles( outfiles, 3, timeoutms=500 ):
        if h:
            print '%s: %s' % ( h.name, line )

    net.stop()
