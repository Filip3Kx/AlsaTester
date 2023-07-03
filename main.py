import fabric
import os
import sys
from capture import *
from playback import * 
from getpass import getpass

class main():
    sys.tracebacklimit=0
    def userInfoGet(self):
        self.ip=input("DUT IP: ")
        self.user=input("Username: ")
        self.password=getpass("Password: ")

    def getAudioDevices(self):
        os.system("cls")
        try:
            result = fabric.Connection(self.ip, user=self.user, connect_kwargs={'password': self.password} ).run('aplay -l | grep -v "Subdev" && arecord -l | grep -v "Subdev"')
        except:
            pass
            print("Something went wrong, Check your credentials, IP or Network connection")
        return result
    
    def cleanUp():
        #remove temporary dir on dut and ctrlr
        print(1)
    def __init__(self):
        super().__init__()
        self.userInfoGet()
        while True:
            self.getAudioDevices()
            testType = input("\n\nDo you want to test\n\t 1. Playback (Remember to start recording on the controller)\n\t 2. Capture (Remember to start playing on the controller)\n")
            if testType=="1":
                playbackCommand.commandGen(self)
            elif testType=="2":
                captureCommand.commandGen(self)
                captureCommand.downloadRecording(self)
            else:
                print("Wrong Choice")

m = main()