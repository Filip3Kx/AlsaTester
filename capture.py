import fabric
import pysftp
import subprocess
import winapps
import os

class captureCommand():
        def commandGen(self):
            dev = input("Choose the device that you want to test: ")
            channel_count = input("Choose channel count: ")
            format_le = input("Choose format: ")
            freq = input("Choose frequency: ")
            try:
                result = fabric.Connection(self.ip, user=self.user, connect_kwargs={'password': self.password} ).run('arecord -Dhw:'+dev+' -c '+channel_count+' -f '+format_le+' -r '+freq+' test.wav -d 15 -vv')
            except:
                print("Command failed, check your inputs")
        
        def downloadRecording(self):
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            try:
                conn = pysftp.Connection(host=self.ip, port=22, username=self.user, password=self.user, cnopts=cnopts)
                print("SFTP connection established...")
            except:
                print("SFTP connection failed")
            
            isAudacity = False
            for element in winapps.list_installed():
                if "Audacity" in str(element):
                    isAudacity=True
                    audacity_path=str(element.install_location) + r"\Audacity.exe"  
            if isAudacity==False: 
                print("Audacity is not installed")

            tmpdir_path = os.getcwd() + r"\Temporary"
            if not os.path.isdir(os.getcwd() + r"\Temporary"):
                print("Creating TMP directory...")
                os.mkdir(tmpdir_path)
            print("Getting the file...")
            conn.get("test.wav", tmpdir_path + r"\test.wav")
            print("Opening Audacity")
            subprocess.Popen([audacity_path, tmpdir_path + r"\test.wav"])
            conn.close()