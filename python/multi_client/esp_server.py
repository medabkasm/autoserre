
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

STATUS_FLAG = ""

def handler(clientConnection,clientAddress,dataWriter):

    global STATUS_FLAG
    try:
        if STATUS_FLAG == "STR":
            print(CYELLOW+"begin receiving data from client {}".format(clientAddress)+CEND)
            clientConnection.send(STATUS_FLAG.encode("ascii")) # start flag to begin data transmission
            print(CGREEN+"{} flag sent to the client {}".format(STATUS_FLAG,clientAddress)+CEND)
            time.sleep(1) # wait 1 sec for client
            print(CYELLOW+"start receiving data from client {}\n".format(clientAddress)+CEND)
            while True:
                data = clientConnection.recv(1024)
                data = data.decode().rstrip("\r\n") # decode incoming data from binary(Bytes) to ascii

                if data:
                    if "END" in data:
                        STATUS_FLAG = "STP"
                        clientConnection.send(STATUS_FLAG.encode("ascii")) # stop flag to stop data transmission
                        data = clientConnection.recv(1024).decode().rstrip("\r\n") # receive flag from the client
                        clientConnection.close()
                        if "RECV" in data:
                            return 1

                    rowData = ["HUM%",data,str(datetime.now())] # for csv file
                    txtData = str("HUM%" + " , " + data + " , " + str(datetime.now()) + "\n") # for txt file
                    savingStatus = dataWriter.add_data(rowData) # store data in the csv file
                    if savingStatus == 0:
                        print(rowData)
                    else:
                        return -1
                else:
                    return -1



    except Exception as err:
        print(CRED+"Error :: connection closed from client :: {}".format(str(err))+CEND)
        return -1


def main():

    global STATUS_FLAG
    obj = Deployement() # create object for deployement
    if obj.drive_auth(): # authentication with google drive api
        driveAuthStatus = True
    else:
        driveAuthStatus = False

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as serverSocket:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensuer reusability of socket connection
        serverSocket.bind((HOST,PORT)) # bind the socket to the specified host,port


        threads = []
        RUN = True
        while RUN:
            serverSocket.listen(5) # listen to the clients(ESP)
            fileFormat = ".csv"
            fileName = "data" + str(datetime.now()) + fileFormat
            savingData = Saving(fileName)
            fileStatus = savingData.create_file()

            if fileStatus == 0:
                STATUS_FLAG = "STR" # start
                while True:
                    try:
                        clientConnection , clientAddress = serverSocket.accept() # accepting the ESP connection
                        # handle the client
                        clientThread = threading.Thread(target = handler , args = (clientConnection,clientAddress,savingData,) )
                        threads.append(clientThread)
                        clientThread.start()

                        for thread in threads:
                            thread.join()

                        savingData.close_file()
                        # deploy
                    except Exception as err:
                        print(CRED+"Error :: during handling threads / clients :: ".format(str(err)))
                        break

                    break
            else:
                RUN = False
                break







main()
