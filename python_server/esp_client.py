import socket
import time
from random import random

HOST = "127.0.0.1"
PORT = 65432

def authentication(clientConnection,userName,password):
    clientConnection.connect((HOST,PORT)) # connect to the server
    credentials = userName + "--" + password
    clientConnection.send(credentials.encode("ascii")) # perform authentication - send username--password
    while True:
        authStatus = clientConnection.recv(1024).decode().rstrip("\r\n")
        if authStatus == "1":
            print("connection established with {} on port {}\n".format(HOST,PORT))
            return 1
        else:
            print("authentication failed\n")
            return -1


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as clientSocket:
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensuer reusability of socket connection
        authentication(clientSocket,"mohamed","1234")

        # test data sending
        while True:
            clientSocket.send(str(int(random()*100)).encode("ascii")) # perform authentication - send username--password
            time.sleep(0.5)
