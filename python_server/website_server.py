import socket # for main program
import hashlib
from datetime import datetime
from saving import Saving
from authentication import Authentication

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
        # test data receiving
        if authStatus == 0:

            savingData = Saving("data.csv")
            csvWriterStatus = savingData.create_file()

            if csvWriterStatus != -1:
                while True:
                    data = clientConnection.recv(1024)
                    data = data.decode().rstrip("\r\n") # decode incoming data from binary(Bytes) to ascii
                    rowData = ["HUM%",data,str(datetime.now())] # for csv file
                    txtData = str("HUM%" + " , " + data + " , " + str(datetime.now()) + "\n") # for txt file
                    savingStatus = savingData.add_data(rowData) # store data in the csv file
                    if savingStatus == 0:
                        print(rowData)
                    else:
                        break

        else:
            print("authentication failed")

if __name__ == "__main__":
    main()
