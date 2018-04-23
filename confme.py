def printConfiguration(net):
    print "Host\tInterface\tIP\t\tMAC"
    hostlist = net.items()
    for h in hostlist:
        nod = net.get(str(h[1]))
        itf = nod.intfNames()
        for i in itf:
            print nod, "\t", i, "\t", nod.IP(str(i)), "\t", nod.MAC(str(i))

    print "\nLINKS"
    #    links = net.topo.links(withInfo = True, withKeys = True, sort=True )
    links = net.topo.links()
    print "From-To\t\tBandwidth\tDelay\tLoss\tInterfaces"
    for l in links:
        #	attr = l[3]
        src = net.get(l[0])
        dest = net.get(l[1])
        conn = src.connectionsTo(dest)
        #	print src, "-", dest, "\t", attr['bw'], "Mbps\t", attr['delay'], "\t", attr['loss'], "%\t", conn
        print src, "-", dest, "\t", conn, " ", l
    print "\nRouting table of h1"
    print net.get("h1").cmd("route -n")


def configureRouting(net):
    hosts = dict()
    for i in range(1, len(net.items()) + 1):
        try:
            hst = net.get('h' + str(i))
            hosts['h' + str(i)] = hst
            hst.cmd('sysctl net.ipv4.ip_forward=1')
            hst.setIP('192.168.1.%s' % str(i), 24, 'h%s-eth0' % str(i))
            hst.setMAC('AA:AA:AA:AA:AA:0%s' % str(i), 'h%s-eth0' % str(i))
            hst.cmd('route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.%s dev h%s-eth0' % (str(i), str(i)))
        except:
            break

    net.pingAll()
    swc = net.get('switch')
    hst.cmd('sysctl net.ipv4.ip_forward=1')
    for hst in hosts:
        swc.setIP('192.168.2.%s' % hst[-1], 24, 'switch-eth%s' % (int(hst[-1]) - 1))
        swc.setMAC('AA:AA:AA:AA:AA:1%s' % hst[-1], 'switch-eth%s' % (int(hst[-1]) - 1))
        swc.cmd('route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.2.%s dev switch-eth%s' % (
        (int(hst[-1]) - 1), (int(hst[-1]) - 1)))
    hosts['switch'] = swc
    net.staticArp()


configureRouting(net)
printConfiguration(net)
