import hashlib # for authentication module
from datetime import datetime
from colors import *


USERNAME = "mohamed"  # predefined username and passowrd
PASSWORD = "1234"
userMD5 = hashlib.md5(USERNAME.encode("ascii")).digest()
passwordMD5 = hashlib.md5(PASSWORD.encode("ascii")).digest()



class Authentication: # class responsible for authentication phase

    def __init__(self,clientConnection,user,password):
        self.user = user
        self.password = password
        self.userMD5 = hashlib.md5(self.user.encode("ascii")).digest()
        self.passMD5 = hashlib.md5(self.password.encode("ascii")).digest()
        self.clientConnection = clientConnection # bounded socket

    def test_authentication(self): # function responsibles for authentication phase

        attempts = 3 # login attempts number to prevent bruteforce attack

        while True:
            clientConnection.send("\nuser name : ".encode("ascii"))
            userName = clientConnection.recv(1024) # get user name from ESP client
            userName = userName.decode().rstrip("\r\n") # decode string from binary(Bytes) to ascii and remove \r\n from the end of the it

            print(CYELLOW+"authentication request from : {} at {} ".format(userName,datetime.now())+CEND)

            if userName == self.user:
                self.clientConnection.send("password : ".encode("ascii"))
                passwordd = self.clientConnection.recv(1024)
                passwordd = passwordd.decode("ascii").rstrip("\r\n")
                if passwordd == self.password:
                    self.clientConnection.send("\nauthentication done ...\n".encode("ascii"))
                    print(CGREEN+"connecting with {} :: {}\n".format(userName,datetime.now())+CEND)
                    return 0
                else:
                    self.clientConnection.send("\npassword incorrect".encode("ascii"))
                    if attempts > 0:
                        attempts = attempts - 1
                        continue
                    else:
                        self.clientConnection.send("\nauthentication failed".encode("ascii"))
                        self.clientConnection.close()
                        return -2
            else:
                if attempts > 0:
                    attempts = attempts - 1
                    self.clientConnection.send("\ninvalid username".encode("ascii"))
                    continue
                else:
                    self.clientConnection.send("\nauthentication failed".encode("ascii"))
                    self.clientConnection.close()
                    return -1


    def esp_authentication(self):
        userNamePassword = self.clientConnection.recv(1024) # get user name from ESP client
        userNamePassword = userNamePassword.decode().rstrip("\r\n") # decode string from binary(Bytes) to ascii and remove \r\n from the end of the it
        try:
            userName , password = userNamePassword.split("--") # separate between username and password  , eg: username--password
        except:
            print(CRED+"bad credentials , authentication failed"+CEND)
            return -1

        userNameMD5 = hashlib.md5(userName.encode("ascii")).digest()
        password_MD5 = hashlib.md5(password.encode("ascii")).digest()
        print(CYELLOW+"authentication request from : {} at {} ".format(userName,datetime.now())+CEND)
        if userNameMD5 == userMD5 and password_MD5 == passwordMD5:
            self.clientConnection.send("1".encode("ascii")) # connection flag , 1 for connected
        else:
            self.clientConnection.send("-1".encode("ascii")) # connection flag , -1 for connection failed ,bad authentication
            print(CRED+"bad credentials , authentication failed"+CEND)
            return -2

        print(CGREEN+"connecting with {} :: {}\n".format(userName,datetime.now())+CEND)
        return 0
