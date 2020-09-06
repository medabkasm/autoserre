from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import random
import time

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
            print("Authentication with api is done successfully")
        except Exception as err:
            print("Error :: api authentication failed :: {}".format(str(err)))
            return -1

    def set_data(self,filePath,title=''): # create title under this format : eg: HUM%_date.txt or TEMP_date.csv

        if filePath:
            self.filePath = filePath
        else:
            print("Error :: invalid file path {}".format(filePath))
            return -1
        try:
            self.dataFile = self.drive.CreateFile()
        except Exception as err:
            print("Error :: cannot create file :: {}".format(str(err)))
            return -1

        if title:
            self.dataFile['title'] = title

        try:
            self.dataFile.SetContentFile(self.filePath)
            print("data file setted successfully for drive uploading")
            return 1
        except Exception as err:
            print("Error :: cannot set data properly :: {}".format(str(err)))
            return -1

    def upload_file(self):
        try:
            self.dataFile.Upload()
            print("File {} uploaded successfully".format(self.filePath))
            return 1
        except Exception as err:
            print("Error :: file {} cannot be uploaded :: {}".format(self.filePath,str(err)))
            return -1
