
from colors import *
import time
from datetime import datetime

global STATUS_FLAG
def handler(clientConnection,clientAddress,dataWriter):
    global STATUS_FLAG
    while True:
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

                    if "END" in data:
                        STATUS_FLAG = "STP"
                        clientConnection.send(STATUS_FLAG.encode("ascii")) # stop flag to stop data transmission
                        clientConnection.recv("RECV".encode("ascii")) # receive flag from the client
                        return

                    rowData = ["HUM%",data,str(datetime.now())] # for csv file
                    txtData = str("HUM%" + " , " + data + " , " + str(datetime.now()) + "\n") # for txt file
                    savingStatus = dataWriter.add_data(rowData) # store data in the csv file
                    if savingStatus == 0:
                        print(rowData)
                    else:
                        return -1



        except Exception as err:
            print(CRED+"Error :: connection closed from client :: {}".format(str(err))+CEND)
            return -1
