import socket
import time
import struct
import threading
import sys
import datetime

h2eth0 = ("192.168.8.2", 1903)
h2eth1 = ("192.168.64.2", 1453)
h1eth0 = ("192.168.2.1", 1881)
h1eth1 = ("192.168.16.1", 1923)

normal ="bastan"
traverse = "sondan"

packetNums = range(10*1000*1000 / 996+1)
size = 10*1000*1000 / 996+1
threadLock = threading.Lock()
readLock = threading.Lock()
sockLock = threading.Lock()

timeCount = 0

sTime = datetime.datetime.now()
eTime = datetime.datetime.now()
RTTList = []
ACKCount = []
ACKList = []

dataSize = 1000
threads = []
f = open('input.txt','rb')
out = open('out.txt','w')
destroyed = False

def ACKWaiter(sock, typeoffunc):

    checksumServerSide = 0
    checksumClientSide = -1
    try:
        data, addr = sock.recvfrom(4)
        if(data=="fini"):
            del packetNums[:]

        checksumServerSide = data[2:4]
        checksumServerSide = struct.unpack('<H',checksumServerSide)[0]
        checksumClientSide = struct.pack('<H',checksum(data[0:2]))
        checksumClientSide = struct.unpack('<H',checksumClientSide)[0]
    except socket.timeout:
        return

    if checksumClientSide == checksumServerSide:
        sequence = struct.unpack('<H',data[0:2])[0]
        threadLock.acquire()
        try:
			del packetNums[packetNums.index(sequence)]
			eTime = datetime.datetime.now()
			ACKList.append(1)
        except:
			eTime = datetime.datetime.now()
        threadLock.release()

def sendAll(sock, nxHost):
    timeExpire=0
    count = 0
    littleThreads = []
    del ACKList[:]
    for i in packetNums:
        try:
            readLock.acquire()
            f.seek(i*996)
            if(i==size-1):
                bin_data = f.read(160)
            else:
                bin_data = f.read(1000)
            #print "type is:",type(bin_data)
            readLock.release()
            sequence = struct.pack('<H',i)

            if(i==size-1):
                bin_data = list(bin_data)
                bin_data.append(sequence[0])
                bin_data.append(sequence[1])
                bin_data = ''.join(bin_data)
                check = struct.pack('<H',checksum(bin_data[0:162]))
                bin_data = list(bin_data)
                bin_data.append(str(check)[0])
                bin_data.append(str(check)[1])
                bin_data = ''.join(bin_data)
            else:
                bin_data = list(bin_data)
                bin_data[-4] = sequence[0]
                bin_data[-3] = sequence[1]
                bin_data = ''.join(bin_data)
                check = struct.pack('<H',checksum(bin_data[0:998]))
                bin_data = list(bin_data)
                bin_data[-2] = str(check)[0]
                bin_data[-1] = str(check)[1]
                bin_data = ''.join(bin_data)

            sock.sendto(bin_data, nxHost)
            #print "packet number ", i, " is sent with length ", len(packetNums)
            #out.write("packet number "+str(i)+ " is sent with length "+ str(len(packetNums))+"\n")
            t = threading.Thread(target=ACKWaiter, args = [sock, normal])
            littleThreads.append(t)
            t.start()
        except:
            readLock.release()

    for th in littleThreads:
        th.join()
    del littleThreads[:]
    print sTime , "--", eTime
    if(len(ACKList) > 0 and eTime != sTime):
    	print sTime , "--", eTime , "-- when times are not equal"
        RTTList.append((eTime - sTime).total_seconds() * 1000)
        ACKCount.append(len(ACKList))
    1

def sendAllTraverse(sock, nxHost):
    timeExpire=0
    littleThreads = []
    del ACKList[:]
    for i in packetNums[::-1]:
        try:
            readLock.acquire()
            f.seek(i*996)
            if(i==size-1):
                bin_data = f.read(160)
            else:
                bin_data = f.read(1000)
            #print "type is:",type(bin_data)
            readLock.release()
            sequence = struct.pack('<H',i)

            if(i==size-1):
                bin_data = list(bin_data)
                bin_data.append(sequence[0])
                bin_data.append(sequence[1])
                bin_data = ''.join(bin_data)
                check = struct.pack('<H',checksum(bin_data[0:162]))
                bin_data = list(bin_data)
                bin_data.append(str(check)[0])
                bin_data.append(str(check)[1])
                bin_data = ''.join(bin_data)
            else:
                bin_data = list(bin_data)
                bin_data[-4] = sequence[0]
                bin_data[-3] = sequence[1]
                bin_data = ''.join(bin_data)
                check = struct.pack('<H',checksum(bin_data[0:998]))
                bin_data = list(bin_data)
                bin_data[-2] = str(check)[0]
                bin_data[-1] = str(check)[1]
                bin_data = ''.join(bin_data)

            sock.sendto(bin_data, nxHost)
            #print "packet number ", i, " is sent with length ", len(packetNums)
            #out.write("packet number "+str(i)+ " is sent with length "+ str(len(packetNums))+"\n")
            t = threading.Thread(target=ACKWaiter, args = [sock, traverse])
            littleThreads.append(t)
            t.start()
        except:
            readLock.release()

    for th in littleThreads:
        th.join()
    del littleThreads[:]
    if(len(ACKList) > 0):
        RTTList.append(eTime - sTime)
        ACKCount.append(len(ACKList))
    1

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
    startTime = time.time()
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock1.bind(h1eth0)
    sock1.settimeout(0.2)
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock2.bind(h1eth1)
    sock2.settimeout(0.2)

    while len(packetNums) > 0:
        eTime = datetime.datetime.now()
        sTime = datetime.datetime.now()
        RTTList = []
        ACKList = []
        t0 = threading.Thread(target = sendAll, args = [sock1, h2eth0, ])
        t1 = threading.Thread(target=sendAllTraverse, args = [sock2, h2eth1])
        threads.append(t0)
        threads.append(t1)
        t0.start()
        t1.start()
        t0.join()
        t1.join()

    sock1.close()
    sock2.close()
    endTime = time.time()
    print "time is:", endTime-startTime
    print RTTList
    print ACKCount
