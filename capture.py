import pysftp
import subprocess
import winapps
import os
import tkinter as tk
from tkinter import END
import time
REFRESH_INTERVAL = 0.1  # Adjust the refresh interval here (in seconds)
LINES_TO_SKIP = 26

class captureCommand():
        def commandGen(self, dev, channel, format_le, freq, file, text1, text2, duration):
            text1.configure(state=tk.NORMAL)
            text2.configure(state=tk.NORMAL)
            text1.delete("1.0", tk.END)
            text2.delete("1.0", tk.END)
            cmd = f'''python -c "import sys;import fabric;sys.tracebacklimit=0; fabric.Connection('{self.ip}', user='{self.user}', connect_kwargs={{'password': '{self.password}'}}).run('arecord -Dhw:{dev} -c {channel} -f {format_le} -r {freq} {file} -d {duration} -vv')"'''
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as process:
                line_count = 0  # Counter to track the number of lines

                for line in process.stdout:
                    line = line.rstrip('\n')  # Remove trailing newline character
                    line_count += 1

                    if line_count <= LINES_TO_SKIP:
                        text1.insert(END, line + '\n')
                    else:
                        text2.delete("1.0", END)  # Clear previous line
                        text2.insert(END, line)

                        text1.see(END)  # Scroll to the end of text_area1

                        text2.update()
                        time.sleep(REFRESH_INTERVAL)

            process.poll()
            if process.returncode != 0:
                raise Exception("An error occurred during the process.")

            text1.configure(state=tk.DISABLED)
            text2.configure(state=tk.DISABLED)
        
        def downloadRecording(self):
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            try:
                conn = pysftp.Connection(host=self.ip, port=22, username=self.user, password=self.user, cnopts=cnopts)
                self.status_label.config(text="SFTP connection established", fg="black")
            except:
                self.status_label.config(text="SFTP connection failed", fg="red")
            
            isAudacity = False
            for element in winapps.list_installed():
                if "Audacity" in str(element):
                    isAudacity=True
                    audacity_path=str(element.install_location) + r"\Audacity.exe"  
            if isAudacity==False: 
                print("Audacity is not installed")

            tmpdir_path = os.getcwd() + r"\Temporary"
            if not os.path.isdir(os.getcwd() + r"\Temporary"):
                self.status_label.config(text="Creating TMP directory...", fg="black")
                os.mkdir(tmpdir_path)
            self.status_label.config(text="Getting the file...", fg="black")
            conn.get("test.wav", tmpdir_path + r"\test.wav")
            self.status_label.config(text="Opening Audacity...", fg="black")
            subprocess.Popen([audacity_path, tmpdir_path + r"\test.wav"])
          