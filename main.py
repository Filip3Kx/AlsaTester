import fabric
import os
from capture import *
from playback import * 
import tkinter as tk
import shutil
import gui
import threading

FILES_TO_CLEANUP=[]
#Fix Upload on playback

class App(tk.Tk):

    def guiInit(self):
        gui.guiInit(self)

    def userInfoGet(self):
        self.ip=self.ip_entry.get()
        self.user=self.user_entry.get()
        self.password=self.password_entry.get()
    
    def captureInfoGet(self):
        self.dev=self.cp_dev_entry.get()
        self.channel=self.cp_channel_entry.get()
        self.format=self.cp_format_entry.get()
        self.freq=self.cp_freq_entry.get()
        self.file=self.cp_file_entry.get()
        self.duration=self.duration_entry.get()

    def playbackInfoGet(self):
        self.dev=self.pb_dev_entry.get()
        self.channel=self.pb_channel_entry.get()
        self.format=self.pb_format_entry.get()
        self.freq=self.pb_freq_entry.get()
        self.file=self.pb_file_entry
        self.duration=self.duration_entry.get()

    def getAudioDevices(self):
        try:
            self.text_area.configure(state=tk.NORMAL)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, fabric.Connection(self.ip, user=self.user, connect_kwargs={'password': self.password} ).run('aplay -l | grep -v "Subdev" && arecord -l | grep -v "Subdev"'))
            self.text_area.configure(state=tk.DISABLED)
            self.status_label.config(text="Connection established with " + self.ip, fg="green")
        except:
            self.text_area.configure(state=tk.NORMAL)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "Something went wrong, Check your credentials, IP or Network connection")
            self.text_area.configure(state=tk.DISABLED)
            self.status_label.config(text="Connection with " + self.ip + " failed", fg="red")
    
    def connectButtonAction(self):
        self.userInfoGet()
        self.status_label.config(text="Connecting to " + self.ip + "...")
        self.getAudioDevices()
    
    def playbackButtonAction(self):
        self.playbackInfoGet()
        self.status_label.config(text="Uploading audio file onto DUT...", fg="black")
        file_name=playbackCommand.uploadSinus(self, self.ip, self.user, self.password, self.file)
        FILES_TO_CLEANUP.append(file_name)
        try:
            self.status_label.config(text="Performing playback test...", fg="black")
            playbackCommand.commandGen(self, self.dev, self.channel, self.format, self.freq, file_name, self.text_area, self.text_area2, self.duration)
        except:
            self.text_area.configure(state=tk.NORMAL)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "Something went wrong. Check connection to the platform, command switches, or the format of the file that you want to play")
            self.text_area.configure(state=tk.DISABLED)
            self.status_label.config(text="Playback failed", fg="red")
            return 0
        self.connectButtonAction()
        self.text_area2.configure(state=tk.NORMAL)
        self.text_area2.delete("1.0", tk.END)
        self.text_area2.configure(state=tk.DISABLED)

    def captureButtonAction(self):
        self.captureInfoGet()
        try:
            self.status_label.config(text="Performing capture test...", fg="black")
            captureCommand.commandGen(self, self.dev, self.channel, self.format, self.freq, self.file, self.text_area, self.text_area2, self.duration)
        except:
            self.text_area.configure(state=tk.NORMAL)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "Something went wrong. Check connection to the platform or command switches")
            self.text_area.configure(state=tk.DISABLED)

            self.status_label.config(text="Capture failed", fg="red")
            return 0
        captureCommand.downloadRecording(self)
        self.connectButtonAction()
        self.text_area2.configure(state=tk.NORMAL)
        self.text_area2.delete("1.0", tk.END)
        self.text_area2.configure(state=tk.DISABLED)

    def cleanUp(self):
        if os.path.isdir(os.getcwd() + r"\Temporary"):
            shutil.rmtree(os.getcwd() + r"\Temporary")
        self.destroy()

        if self.ip:
            for query in FILES_TO_CLEANUP:
                fabric.Connection(self.ip, user=self.user, connect_kwargs={'password': self.password}).run('rm ' + query)

    def connectThread(self):
        cn_thread = threading.Thread(target=self.connectButtonAction)
        cn_thread.start()
    
    def playbackThread(self):
        pb_thread = threading.Thread(target=self.playbackButtonAction)
        pb_thread.start()
    
    def captureThread(self):
        cp_thread = threading.Thread(target=self.captureButtonAction)
        cp_thread.start()

    def __init__(self):
        super().__init__()
        self.guiInit()
        isAudacity = False
        for element in winapps.list_installed():
            if "Audacity" in str(element):
                isAudacity=True
        if isAudacity==False: 
            self.status_label.config(text="Audacity is not installed", fg="red")
        else:
            self.status_label.config(text="Audacity is installed", fg="green")

        self.protocol("WM_DELETE_WINDOW", self.cleanUp)

        

if __name__ == "__main__":
    app = App()
    app.mainloop()