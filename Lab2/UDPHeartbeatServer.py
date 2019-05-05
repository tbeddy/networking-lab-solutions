"""
Lab 1: UDP Pinger Lab

This server listens for heartbeats from a single client and sends back messages regarding any
missing packets and the time difference between packets.

Adapted from UDPPingerServer.py
"""

# We will need the following module to generate randomized lost packets
import random
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 12000))
# Wait five seconds before assuming client has stopped
serverSocket.settimeout(5.0)

lastSequenceNumber = 0
lastTimeStamp = 0
while True:
    try:
        # Generate random number in the range of 0 to 10
        rand = random.randint(0, 10)
        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)
        # Separate the message into sequence number and timestamp
        messageParts = message.decode().split()
        receivedSequenceNumber = int(messageParts[0])
        receivedTimeStamp = float(messageParts[1])

        # If rand is less than 4, we consider the packet lost and do not respond
        if rand < 4:
            continue

        # Otherwise, the server responds
        if (receivedSequenceNumber > (lastSequenceNumber + 1)):
            # If there are multiple missing packets, send a message for each
            for i in range(lastSequenceNumber + 1, receivedSequenceNumber + 1):
                missingPacketMessage = "Missing Packet: {}".format(i)
                serverSocket.sendto(missingPacketMessage.encode(), address)

        if ((lastSequenceNumber > 0) and (lastTimeStamp > 0)):
            timeDifference = receivedTimeStamp - lastTimeStamp
            timeStampMessage = "Time between {} and {}: {}".format(lastSequenceNumber,
                                                                   receivedSequenceNumber,
                                                                   timeDifference)
            serverSocket.sendto(timeStampMessage.encode(), address)
            
        lastSequenceNumber = receivedSequenceNumber
        lastTimeStamp = receivedTimeStamp
    except timeout:
        lastSequenceNumber = 0
        lastTimeStamp = 0
