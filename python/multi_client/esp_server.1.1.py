
import socket # for main program
import hashlib
from datetime import datetime
from saving import Saving
from authentication import Authentication
from drive_deployement import Deployement
import os
import json
from colors import *
import threading
import time


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on

CREATED_FILE = True
FILE_WRITER = None


def handler(clientConnection,clientAddress):

    global CREATED_FILE
    global FILE_WRITER
    STATUS_FLAG = "STR"

    while CREATED_FILE != True:
        while True:
            try:
                if STATUS_FLAG == "STR":

                    print(CYELLOW+"begin receiving data from client {}".format(clientAddress)+CEND)
                    clientConnection.send(STATUS_FLAG.encode("ascii")) # start flag to begin data transmission
                    print(CGREEN+"{} flag sent to the client {}".format(STATUS_FLAG,clientAddress)+CEND)
                    print(CYELLOW+"start receiving data from client {}\n".format(clientAddress)+CEND)

                    while True:
                        data = clientConnection.recv(1024)
                        data = data.decode().rstrip("\r\n") # decode incoming data from binary(Bytes) to ascii

                        if data:
                            if "END" in data:
                                STATUS_FLAG = "STP"
                                clientConnection.send(STATUS_FLAG.encode("ascii")) # stop flag to stop data transmission
                                data = clientConnection.recv(1024).decode().rstrip("\r\n") # receive flag from the client
                                if "RECV" in data:
                                    FILE_WRITER.close_file()
                                    #clientConnection.close()
                                    CREATED_FILE = True
                                    STATUS_FLAG = "STR"
                                    break

                            rowData = [clientAddress[0],clientAddress[1],"HUM%",data,str(datetime.now())] # for csv file

                            txtData = str(clientAddress[0]) + " , " + str(clientAddress[1]) + " , " + "HUM%" + " , " + data + " , " + str(datetime.now()) + "\n"# for txt file
                            savingStatus = FILE_WRITER.add_data(rowData) # store data in the csv file
                            if savingStatus == 0:
                                print(txtData)

                        else:
                            return -1


            except Exception as err:
                print(CRED+"Error :: connection closed from client {}:: {}".format(clientAddress,str(err))+CEND)
                return -1

def file_handler():
    global CREATED_FILE
    global FILE_WRITER
    while True:
        while CREATED_FILE:
            fileFormat = ".csv"
            fileName = "HUM%" + str(datetime.now()) + fileFormat
            savingData = Saving(fileName)
            fileStatus = savingData.create_file()
            CREATED_FILE = False
            FILE_WRITER = savingData




def main():


    obj = Deployement() # create object for deployement
    if obj.drive_auth(): # authentication with google drive api
        driveAuthStatus = True
    else:
        driveAuthStatus = False

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as serverSocket:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensuer reusability of socket connection
        serverSocket.bind((HOST,PORT)) # bind the socket to the specified host,port
        serverSocket.listen(5) # listen to the clients(ESP)

        threads = []
        superThread = threading.Thread(target = file_handler)
        threads.append(superThread)
        superThread.start()
        while True:
            try:
                clientConnection , clientAddress = serverSocket.accept() # accepting the ESP connection
                # handle the client
                clientThread = threading.Thread(target = handler , args = (clientConnection,clientAddress,) )
                threads.append(clientThread)
                clientThread.start()

            except Exception as err:
                print(CRED+"Error :: during handling threads / clients :: ".format(str(err)))
                break






main()
