import socket # for main program
import hashlib
from datetime import datetime
from saving import Saving
from authentication import Authentication
from drive_deployement import Deployement
import os
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on
USERNAME = "mohamed"  # predefined username and passowrd
PASSWORD = "1234"
userMD5 = hashlib.md5(USERNAME.encode("ascii")).digest()
passwordMD5 = hashlib.md5(PASSWORD.encode("ascii")).digest()


def main():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as serverSocket:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensuer reusability of socket connection
        serverSocket.bind((HOST,PORT)) # bind the socket to the specified host,port
        serverSocket.listen(1) # listen to the only client(ESP)
        clientConnection , clientAddress = serverSocket.accept() # accepting the ESP connection
        authObj = Authentication(clientConnection,"mohamed","1234") # create Authentication object
        authStatus = authObj.esp_authentication() # begin authentication phase
        # start data receiving
        if authStatus == 0:

            obj = Deployement() # create object for deployement
            if obj.drive_auth(): # authentication with google drive api
                driveAuthStatus = True
            else:
                driveAuthStatus = False

            RUN = True
            while RUN:

                fileFormat = ".csv"
                fileName = "data" + str(datetime.now()) + fileFormat
                savingData = Saving(fileName)
                fileStatus = savingData.create_file()
                print("start receiving data from client for {} file\n".format(fileName))
                if fileStatus == 0:
                    while True:
                        try:
                            data = clientConnection.recv(1024)
                            data = data.decode().rstrip("\r\n") # decode incoming data from binary(Bytes) to ascii
                        except Exception as err:
                            print("Error :: connection closed from client :: {}".format(str(err)))
                            RUN = False
                            break

                        if "end" in data :
                            print("\ndone with file {}".format(fileName))
                            # done with 24h data file and upload it to google drive
                            fileStatus = savingData.close_file() # close file writer
                            if fileStatus == 0 and driveAuthStatus:
                                filePath = "./" + fileName
                                if obj.set_data(filePath,fileName): # deploy the created file to google drive
                                    obj.upload_file()

                            clientConnection.send("begin".encode("ascii")) # begin with a new file
                                # delete file from current directory
                            break # break the inner loop to begin with a new file

                        elif "done" in data: # data transfert is done
                            RUN = False
                            print("removing {} file".format(fileName))
                            os.remove("./"+fileName) # remove the last empty file , its a BUG
                            break

                        rowData = ["HUM%",data,str(datetime.now())] # for csv file
                        txtData = str("HUM%" + " , " + data + " , " + str(datetime.now()) + "\n") # for txt file
                        savingStatus = savingData.add_data(rowData) # store data in the csv file
                        if savingStatus == 0:
                            print(rowData)
                        else:
                            RUN = False
                            break

        else:
            print("authentication failed")

if __name__ == "__main__":
    main()
