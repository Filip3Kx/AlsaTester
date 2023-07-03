import subprocess
import tkinter as tk
from tkinter import END
import time
import fabric

REFRESH_INTERVAL = 0.1  # Adjust the refresh interval here (in seconds)
LINES_TO_SKIP = 26

class playbackCommand():
        def commandGen(self, dev, channel, format_le, freq, file, text1, text2, duration):
            text1.configure(state=tk.NORMAL)
            text2.configure(state=tk.NORMAL)
            text1.delete("1.0", tk.END)
            text2.delete("1.0", tk.END)
            cmd = f'''python -c "import sys;import fabric;sys.tracebacklimit=0; fabric.Connection('{self.ip}', user='{self.user}', connect_kwargs={{'password': '{self.password}'}}).run('aplay -Dhw:{dev} -c {channel} -f {format_le} -r {freq} {file} -d {duration} -vv')"'''
            print(cmd)
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

        def uploadSinus(self, ip, user, password, file):
            with fabric.Connection(ip, user=user, connect_kwargs={'password': password}) as conn:
                conn.put(file)
                file_name = file.split("/")[-1]
                print(file_name)
                return file_name
