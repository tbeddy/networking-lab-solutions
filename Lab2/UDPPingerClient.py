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
        message = "Ping {} {}".format(i, originalTime)
        clientSocket.sendto(message.encode(), (args.server_host, serverPort))
        try:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            print(modifiedMessage.decode())
            print("Round Trip Time (RTT): {}".format(time.time() - originalTime))
        except timeout:
            print("Request timed out")

    clientSocket.close()
