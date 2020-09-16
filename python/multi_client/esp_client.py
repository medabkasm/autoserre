import socket
import time
from random import random
from colors import *

HOST = "127.0.0.1"
PORT = 65432
CONN_ATTEMPTS = 0 # reconnection attempts for timout exception

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


RUN = True
oneDay = 10 # seconds in one day

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as clientSocket:
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensuer reusability of socket connection
    #authentication(clientSocket,"mohamed","1234")
    clientSocket.connect((HOST,PORT))

    while RUN:
        try:
            serverStatus = clientSocket.recv(1024).decode().rstrip("\r\n") # receive a to start again data transmissin
            if "STR" in serverStatus:
                print(CGREEN+serverStatus+CEND)
                currentTime = time.time()
                begin = currentTime
                while True:
                    endtime = time.time()
                    if ( endtime - currentTime ) > oneDay :
                        data = "END".encode("ascii") # send a flag to the webserver to upload the daily file to google drive
                        clientSocket.send(data)
                        serverStatus = clientSocket.recv(1024).decode().rstrip("\r\n") # receive a to start again data transmission
                        print(CGREEN+serverStatus+CEND)
                        if "STP" in serverStatus:
                            serverStatus = "RECV"
                            clientSocket.send(serverStatus.encode("ascii"))
                            print(CYELLOW+serverStatus+CEND)
                            time.sleep(4)
                            break

                    data = str(int(random()*100)).encode("ascii") # data readed from esp
                    clientSocket.send(data) # send data to the webserver
                    time.sleep(0.5)

        except Exception as err :
            print(CRED+"Error :: connection error :: {}".format(str(err))+CEND)
            RUN = False
            break
