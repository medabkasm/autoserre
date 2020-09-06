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

    currentTime = time.time()
    oneDay = 10 # seconds in one day
    begin = currentTime
    while True:
        endtime = time.time()
        if ( endtime - currentTime ) > oneDay :
            data = "end".encode("ascii") # send a flag to the webserver to upload the daily file to google drive
            clientSocket.send(data)
            serverStatus = clientSocket.recv(1024).decode().rstrip("\r\n") # receive a to start again data transmission
            if "begin" in serverStatus:
                currentTime = time.time()
                continue
        elif ( endtime - begin ) > 60 :
            break

        data = str(int(random()*100)).encode("ascii") # data readed from esp
        clientSocket.send(data) # send data to the webserver
        time.sleep(0.5)



    clientSocket.send("done".encode("ascii"))
    print("transfert completed")
