"""
Lab 1: Web Server Lab (Multithreaded Version)
"""

#import socket module
from socket import *
import sys #In order to terminate the program
import threading

#Function to thread each client socket
def client_thread(connectionSocket):
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        #Send one HTTP header line into socket
        connectionSocket.send("Accept-Encoding: gzip, deflate\r\n".encode())
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        for c in "404 Not Found":
            connectionSocket.send(c.encode())
        connectionSocket.send("\r\n".encode())
        #Close client socket
        connectionSocket.close()

if __name__ == "__main__":
    serverSocket = socket(AF_INET, SOCK_STREAM)
    #Prepare a server socket
    serverPort = 6789
    serverSocket.bind(('', serverPort))
    serverSocket.listen()
    while True:
        #Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        new_thread = threading.Thread(target=client_thread, args=(connectionSocket,))
        new_thread.start()

    serverSocket.close()
    sys.exit() #Terminate the program after sending the corresponding data
