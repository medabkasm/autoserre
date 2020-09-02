import socket
import hashlib
from datetime import datetime

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on


def authentication(sock): # function responsibles for authentication phase
    user ="mohamed"
    passwordd = "1234"
    attempts = 3 # login attempts number

    while True:
        clientConnection.send("\nuser name : ".encode("ascii"))
        userName = clientConnection.recv(1024) # get user name from ESP client
        userName = userName.decode().rstrip("\r\n") # decode string from binary(Bytes) to ascii and remove \r\n from the end of the it

        print("authentication request form : {} at {} ".format(userName,datetime.now()))

        if userName == user:
            clientConnection.send("password : ".encode())
            password = clientConnection.recv(1024)
            password = password.decode("ascii").rstrip("\r\n")
            if password == passwordd:
                clientConnection.send("password correct".encode("ascii"))
                clientConnection.send("start receiving data ...".encode("ascii"))
                return 1
            else:
                clientConnection.send("\npassword incorrect".encode("ascii"))
                if attempts > 0:
                    attempts = attempts - 1
                    continue
                else:
                    clientConnection.send("\nauthentication failed".encode("ascii"))
                    clientConnection.close()
                    return -2
        else:
            if attempts > 0:
                attempts = attempts - 1
                continue
            else:
                clientConnection.send("\nauthentication failed".encode("ascii"))
                clientConnection.close()
                return -1




with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as serverSocket:
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensuer reusability of socket connection
    serverSocket.bind((HOST,PORT)) # bind the socket to the specified host,port
    serverSocket.listen(1) # listen the only client(ESP)
    clientConnection , clientAddress = serverSocket.accept() # accepting the ESP connection
    authStatus = authentication(serverSocket) # begin authentication phase
    if authStatus == 1:
            while True:
                data = clientConnection.recv(1024)
                try:
                    print(data.decode('ascii')) # decode incoming data from binary(Bytes) to ascii
                except:
                    print("invalid data")
    else:
        print("authentication failed")
