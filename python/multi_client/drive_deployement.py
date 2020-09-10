from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import random
import time
from colors import *

i = 0
data = ""


class Deployement: # class responsible for google drive api

    def __init__(self):
        self.data = ''
        self.drive = None
        self.dataFile = None

    def drive_auth(self): # authentication with settings.yaml file
        try:
            gauth = GoogleAuth()
            # Create local webserver and auto handles authentication.
            gauth.LocalWebserverAuth()
            self.drive = GoogleDrive(gauth)
            return self.drive
            print(CGREEN+"Authentication with api is done successfully"+CEND)
        except Exception as err:
            print(CRED+"Error :: api authentication failed :: {}".format(str(err))+CEND)
            return -1

    def set_data(self,filePath,title=''): # create title under this format : eg: HUM%_date.txt or TEMP_date.csv

        if filePath:
            self.filePath = filePath
        else:
            print(CRED+"Error :: invalid file path {}".format(filePath)+CEND)
            return -1
        try:
            self.dataFile = self.drive.CreateFile()
        except Exception as err:
            print(CRED+"Error :: cannot create file :: {}".format(str(err))+CEND)
            return -1

        if title:
            self.dataFile['title'] = title

        try:
            self.dataFile.SetContentFile(self.filePath)
            print(CGREEN+"data file setted successfully for drive uploading"+CEND)
            return 1
        except Exception as err:
            print(CRED+"Error :: cannot set data properly :: {}".format(str(err))+CEND)
            return -1

    def upload_file(self):
        try:
            self.dataFile.Upload()
            print(CGREEN+"File {} uploaded successfully".format(self.filePath)+CEND)
            return 1
        except Exception as err:
            print(CGRED+"Error :: file {} cannot be uploaded :: {}".format(self.filePath,str(err))+CEND)
            return -1
