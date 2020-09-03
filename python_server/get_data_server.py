import socket
import hashlib
from datetime import datetime
import csv

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on

userMD5 = hashlib.md5("mohamed".encode("ascii")).digest()
passwordMD5 = hashlib.md5("1234".encode("ascii")).digest()

class Authentication:

    def __init__(self,clientConnection,user,password):
        self.user = user
        self.password = password
        self.userMD5 = hashlib.md5(self.user.encode("ascii")).digest()
        self.passMD5 = hashlib.md5(self.password.encode("ascii")).digest()
        self.clientConnection = clientConnection

    def test_authentication(self): # function responsibles for authentication phase

        attempts = 3 # login attempts number

        while True:
            clientConnection.send("\nuser name : ".encode("ascii"))
            userName = clientConnection.recv(1024) # get user name from ESP client
            userName = userName.decode().rstrip("\r\n") # decode string from binary(Bytes) to ascii and remove \r\n from the end of the it

            print("authentication request from : {} at {} ".format(userName,datetime.now()))

            if userName == self.user:
                self.clientConnection.send("password : ".encode("ascii"))
                passwordd = self.clientConnection.recv(1024)
                passwordd = passwordd.decode("ascii").rstrip("\r\n")
                if passwordd == self.password:
                    self.clientConnection.send("\nauthentication done ...\n".encode("ascii"))
                    print("connecting with {} :: {}\n".format(userName,datetime.now()))
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
        userNamePassword = self.clientConnection.recv(4092) # get user name from ESP client
        userNamePassword = userNamePassword.decode().rstrip("\r\n") # decode string from binary(Bytes) to ascii and remove \r\n from the end of the it
        print(userNamePassword)
        try:
            userName , password = userNamePassword.split("--")
        except:
            return -1

        userNameMD5 = hashlib.md5(userName.encode("ascii")).digest()
        password_MD5 = hashlib.md5(password.encode("ascii")).digest()
        print("authentication request from : {} at {} ".format(userName,datetime.now()))
        if userNameMD5 == userMD5 and password_MD5 == passwordMD5:
            self.clientConnection.send("1".encode("ascii"))
        else:
            self.clientConnection.send("-1".encode("ascii"))
            return -2

        print("connecting with {} :: {}\n".format(userName,datetime.now()))
        return 0


class Saving:
    def __init__(self,fileName = "data.csv",separateFiles = False):
        self.fileName = fileName # created file name to store the data
        self.separateFiles = separateFiles # sotre data in separate files or not (humidty data , temperature data ...ect) , False by default
        self.csvWriter = None

    def create_file(self):
        try:
            self.csvDataFile = open(self.fileName,'w') # didn't use 'with' statement for future use of the open file
            self.csvWriter = csv.writer(self.csvDataFile,delimiter = ',')
            print("csv file {} created".format(self.fileName))
            return self.csvWriter
        except Exception as err:
            print("Error with opening csv file :: {}".format(str(err)))

    def add_data(self,data):
        try:
            self.csvWriter.writerows(data) # use the open writer from the create_file methode
            return 1
        except Exception as err :
            print("Error with adding rows :: {}".format(str(err)))
            return -1





with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as serverSocket:
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensuer reusability of socket connection
    serverSocket.bind((HOST,PORT)) # bind the socket to the specified host,port
    serverSocket.listen(1) # listen the only client(ESP)
    clientConnection , clientAddress = serverSocket.accept() # accepting the ESP connection
    authObj = Authentication(clientConnection,"mohamed","1234") # create Authentication object
    authStatus = authObj.esp_authentication() # begin authentication phase
    # test data receiving
    if authStatus == 0:
        savingData = Saving("data.csv")
        csvWriter = savingData.create_file()
        i = 0
        pdfFile = open("dataFile.txt",'w')
        if csvWriter != -1:
            while True:
                data = clientConnection.recv(1024)
                data = data.decode().rstrip("\r\n") # decode incoming data from binary(Bytes) to ascii
                rowData = ["HUM%",data,str(datetime.now())]
                pdfData = "HUM%" + " , " + data + " , " + str(datetime.now()) + "\n"
                savingData.add_data(rowData) # store data in the csv file
                pdfFile.write(pdfData) # store data in text file
                try:
                    print(rowData)
                except:
                    print("invalid data")
    else:
        print("authentication failed")
