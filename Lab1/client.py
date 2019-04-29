from socket import *
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('server_host',
                        help='the server IP address or host name')
    parser.add_argument('server_port', type=int,
                        help='the port at which the server is listening')
    parser.add_argument('filename',
                        help='the path at which the requested object is stored at the server')
    args = parser.parse_args()

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((args.server_host, args.server_port))
    clientSocket.send("GET {} HTTP/1.1\r\n".format(args.filename).encode())
    clientSocket.send("Connection: close\r\n".encode())
    clientSocket.send("\r\n".encode())

    #Don't stop receiving HTTP messages until the packets are empty
    fullMessage = ""
    newestPacket = clientSocket.recv(1024).decode()
    while newestPacket != "":
        fullMessage += newestPacket
        newestPacket = clientSocket.recv(1024).decode()
    print(fullMessage)
    clientSocket.close()
