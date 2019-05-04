"""
Lab 1: UDP Pinger Lab

This client sends ten pings to the included server.
The Round Trip Time is calculated for each ping.
Minimum ping, maximum ping, average ping, and packet loss rate are also calculated.
"""

from socket import *
import argparse
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('server_host',
                        help='the server IP address or host name')
    args = parser.parse_args()

    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1.0)

    allRTTs = []
    for i in range(1, 11):
        originalTime = time.time()
        message = "Ping {} {}".format(i, originalTime)
        clientSocket.sendto(message.encode(), (args.server_host, serverPort))
        try:
            modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
            print(modifiedMessage.decode())
            roundTripTime = time.time() - originalTime
            print("Round Trip Time (RTT): {}".format(roundTripTime))
            allRTTs.append(roundTripTime)
        except timeout:
            print("Request timed out")

    print("Minimum ping: {}".format(min(allRTTs)))
    print("Maximum ping: {}".format(max(allRTTs)))
    print("Average ping: {}".format(sum(allRTTs)/len(allRTTs)))
    print("Packet loss rate: {}%".format(len(allRTTs)*10))

    clientSocket.close()
