"""
Lab 1: UDP Pinger Lab

This client sends ten heartbeats to a server.

Adapted from UDPPingerClient.py
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

    for i in range(1, 11):
        originalTime = time.time()
        message = "{} {}".format(i, originalTime)
        clientSocket.sendto(message.encode(), (args.server_host, serverPort))
        try:
            message, serverAddress = clientSocket.recvfrom(1024)
            print(message.decode())
        except timeout:
            print("Request timed out")

    clientSocket.close()
