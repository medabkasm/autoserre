import csv # for saving module
from colors import *


class Saving:
    def __init__(self,fileName,separateFiles = False):
        self.fileName = fileName # created file name to store the data
        self.fileFormat = self.fileName.split(".")[-1].lower()
        self.separateFiles = separateFiles # sotre data in separate files or not (humidty data , temperature data ...ect) , False by default
        self.__csvWriter = None
        self.__dataFile = None

    def create_file(self):

        if self.fileFormat == "csv" or self.fileFormat == "txt":
            try:
                self.__dataFile = open(self.fileName,"w") # didn't use 'with' statement for future use of the open file
                print(CGREEN+"\nfile {} created".format(self.fileName)+CEND)
            except Exception as err:
                print(CRED+"Error :: file {} cannot be created :: {}".format(str(err))+CEND)

            if self.fileFormat == "csv":
                try:
                    self.__csvWriter = csv.writer(self.__dataFile,delimiter = ',')
                    return 0
                except Exception as err:
                    print(CRED+"Error :: with opening csv writer :: {}".format(str(err))+CEND)
                    return -1
            else:
                return 0
        else:
            print(CRED+"Error :: unkown file format :: supports only .txt and .csv formats"+CEND)
            return -1



    def add_data(self,data):

        if self.fileFormat == "csv":
            if isinstance(data,list):
                try:
                    self.__csvWriter.writerow(data) # use the open writer from the create_file methode
                    return 0
                except Exception as err :
                    print(CRED+"Error :: during with row to {} file :: {}".format(self.__dataFile,str(err))+CEND)
                    return -1
            else:
                print(CRED+"Error :: data for csv file must be a list"+CEND)
                return -1
        else:
            if isinstance(data,str):
                try:
                    data = data.rstrip("\n")
                    self.__dataFile.write(data + "\n")
                    return 0
                except Exception as err:
                    print(CRED+"Error :: during writing data to {} file :: {}".format(self.__dataFile,str(err))+CEND)
                    return -1
            else:
                print(CRED+"Error :: data for txt file must a string"+CEND)
                return -1

    def close_file(self):
        try:
            self.__dataFile.close()
            self.__csvWriter = None
            print(CGREEN+"file {} closed succefully".format(self.fileName)+CEND)
            return 0

        except Exception as err:
            print(CRED+"Error :: cannot close file {} succefully :: {}".format(self.fileName,str(err))+CEND)
            return -1
