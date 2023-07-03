import fabric
import pysftp

class playbackCommand():
        def commandGen(self):
            dev = input("Choose the device that you want to test: ")
            channel_count = input("Choose channel count: ")
            format_le = input("Choose format: ")
            freq = input("Choose frequency: ")
            try:
                result = fabric.Connection(self.ip, user=self.user, connect_kwargs={'password': self.password} ).run('cat /dev/urandom | aplay -Dhw:'+dev+' -c '+channel_count+' -f '+format_le+' -r '+freq+' -d 15 -vv')
            except: 
                print("Command failed, check your inputs")

        def uploadSinus(self):
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            try:
                conn = pysftp.Connection(host=self.ip, port=22, username=self.user, password=self.user, cnopts=cnopts)
                print("SFTP connection established...")
            except:
                print("SFTP connection failed")