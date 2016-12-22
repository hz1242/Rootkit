import threading
import socket
import time
import datetime
import zlib
import json

__author__ = 'Nathaniel Cotton, Zhao Hongyu'

cache = {}
file = open('loggedInfo.txt','w')


class Network:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket.bind((socket.gethostbyname('0.0.0.0'), port))


class ProcessingThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            for addr, value in cache.items():
                toPop = []
                map = value['messageMap']
                for messageID, queue in map.items():
                    self.printMessageResult(addr,messageID,queue)
                    toPop.append(messageID)
                for m in toPop:
                    map.pop(m)
            time.sleep(1)

    def printMessageResult(self, addr, messageID, queue):
        data = ''
        sortedQueue = sorted(queue,key=lambda k:k['index'])
        for msg in sortedQueue:
            data += msg['data']
        #print('{} : {}'.format(str(addr),data))
        file.write('{} : {}\n'.format(str(addr),data))
        file.flush()


class Recv(threading.Thread):
    def __init__(self, network):
        super().__init__()
        self.setDaemon(False)
        self.network = network
        self.addr = None
        self.lastRecvTime = None

    def run(self):
        while True:
            data, addr = self.network.socket.recvfrom(1024)
            data = zlib.decompress(data)
            data = data.decode('UTF-8')
            data = json.loads(data)
            # print(data)
            if addr not in cache:
                cache[addr] = {
                    "lastRecv": datetime.datetime.now(),
                    "messageMap" : {
                        data['message_id'] : [data]
                    }
                }
            else:
                cache[addr]["lastRecv"] = datetime.datetime.now()
                map = cache[addr]['messageMap']
                if data['message_id'] in map:
                    map[data['message_id']].append(data)
                else:
                    map[data['message_id']] = [data]

    def getClients(self):
        self.purge()
        ret = []
        for key, item in cache.items():
            ret.append(key)
        return ret

    def purge(self):
        currentTime = datetime.datetime.now()
        toPurge = []
        for key, value in cache.items():
            lastRecv = value["lastRecv"]
            if (currentTime - lastRecv).total_seconds() > getTimeout():
                toPurge.append(key)
        for key in toPurge:
            cache.pop(key)


def getTimeout():
    return 60


def printClients(clientList):
    for index in range(len(clientList)):
        print('{} : {}'.format(index + 1, clientList[index]))


def main():
    port = 5005
    network = Network(port)
    recv = Recv(network)
    recv.start()
    proc = ProcessingThread()
    proc.start()
    while True:
        try:
            clientList = recv.getClients()
            if len(clientList) == 0:
                print('No Clients')
                time.sleep(5)
            else:
                clientId = 0
                if len(clientList) != 1:
                    printClients(clientList)
                    clientId = int(input("Client: "))
                command = input("Command: ")
                network.socket.sendto(command.encode('UTF-8'), clientList[clientId - 1])
        except Exception as e:
            pass


if __name__ == '__main__':
    main()
