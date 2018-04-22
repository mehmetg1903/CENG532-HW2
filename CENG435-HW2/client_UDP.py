import socket
import time
import struct
import threading
h1eth0 = ("192.168.2.1", 1881)
h1eth1 = ("192.168.16.1", 1923)
h2eth0 = ("192.168.8.2", 1903)
h2eth1 = ("192.168.64.2", 1453)

packetNums = range(10*1000*1000 / 996 + 1)
size = packetNums[-1]
threadLock = threading.Lock()
readLock = threading.Lock()
sockLock = threading.Lock()

dataSize = 1000
f = open('input.txt','rb')

destroyed = False

def ACKWaiter(sock, i, nxHost):
    timeCount = 0
    checksumServerSide = 0
    checksumClientSide = -1

    try:
        readLock.acquire()
        f.seek(i*996)
        if(i==size):
            bin_data = f.read(160)
        else:
            bin_data = f.read(996)
        readLock.release()
        sequence = struct.pack('<H',i)
        bin_data = list(bin_data)
        bin_data.append(sequence[0])
        bin_data.append(sequence[1])
        bin_data = ''.join(bin_data)
        check = struct.pack('<H',checksum(bin_data))
        bin_data = list(bin_data)
        bin_data.append(str(check)[0])
        bin_data.append(str(check)[1])
        bin_data = ''.join(bin_data)
        sock.sendto(bin_data, nxHost)
        #print "packet number ", i, " is sent with length ", len(packetNums)
    except:
        readLock.release()

    try:
        data, addr = sock.recvfrom(4)
        if(data=="fini"):
            del packetNums[:]
            return
        checksumServerSide = data[2:4]
        checksumServerSide = struct.unpack('<H',checksumServerSide)[0]
        checksumClientSide = struct.pack('<H',checksum(data[0:2]))
        checksumClientSide = struct.unpack('<H',checksumClientSide)[0]
    except socket.timeout:
        timeCount += 1
        return

    if checksumClientSide == checksumServerSide:
        sequence = struct.unpack('<H',data[0:2])[0]
        threadLock.acquire()
        try:
            del packetNums[packetNums.index(sequence)]
        except:
            1
        threadLock.release()

def sendAll(sock, nxHost):
    littleThreads = []
    for i in packetNums:
            #print "packet number ", i, " is sent with length ", len(packetNums)
        t = threading.Thread(target=ACKWaiter, args = [sock, i, nxHost])
        littleThreads.append(t)
        t.start()

    for th in littleThreads:
        th.join()
    del littleThreads[:]

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff

if __name__ == "__main__":
	sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock1.settimeout(0.2)
	sock1.bind(h1eth0)
	sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock2.settimeout(0.2)
	sock2.bind(h1eth1)
	threads = []
	while len(packetNums) > 0:
		t0 = threading.Thread(target = sendAll, args = [sock1, h2eth0])
		t0.start()
		t1 = threading.Thread(target = sendAll, args = [sock2, h2eth1])
		threads.append(t1)
		t1.start()

	for thread in threads:
		thread.join()

	sock1.close()
	sock2.close()