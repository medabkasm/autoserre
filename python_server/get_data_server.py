import socket
import hashlib
from datetime import datetime

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on

user ="mohamed"
passwordd = "1234"
userMD5 = hashlib.md5(user.encode("ascii")).digest()
passwordMD5 = hashlib.md5(passwordd.encode("ascii")).digest()

def test_authentication(clientConnection): # function responsibles for authentication phase

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
                clientConnection.send("\nstart receiving data ...\n".encode("ascii"))
                return 0
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
                clientConnection.send("\ninvalid iusername".encode("ascii"))
                continue
            else:
                clientConnection.send("\nauthentication failed".encode("ascii"))
                clientConnection.close()
                return -1


def esp_authentication(clientConnection,user=userMD5,password=passwordMD5):
    userNamePassword = clientConnection.recv(1024) # get user name from ESP client
    userNamePassword = userNamePassword.decode().rstrip("\r\n") # decode string from binary(Bytes) to ascii and remove \r\n from the end of the it
    try:
        userName , password = userNamePassword.split("--")
    except:
        return -1
        
    userNameMD5 = hashlib.md5(userName.encode("ascii")).digest()
    password_MD5 = hashlib.md5(password.encode("ascii")).digest()
    print(userName,password)
    print("authentication request form : {} at {} ".format(userName,datetime.now()))
    if userNameMD5 == userMD5 and password_MD5 == passwordMD5:
        clientConnection.send("1".encode("ascii"))
    else:
        clientConnection.send("-1".encode("ascii"))
        return -1

    return 0


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as serverSocket:
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensuer reusability of socket connection
    serverSocket.bind((HOST,PORT)) # bind the socket to the specified host,port
    serverSocket.listen(1) # listen the only client(ESP)
    clientConnection , clientAddress = serverSocket.accept() # accepting the ESP connection
    authStatus = esp_authentication(clientConnection) # begin authentication phase
    if authStatus == 0:
            while True:
                data = clientConnection.recv(1024)
                try:
                    print(data.decode('ascii')) # decode incoming data from binary(Bytes) to ascii
                except:
                    print("invalid data")
    else:
        print("authentication failed")
