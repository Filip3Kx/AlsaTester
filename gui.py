import tkinter as tk
from tkinter import filedialog, ttk

def guiInit(self):
        #FRAMES
        ssh_frame = tk.Frame(self)
        ssh_frame.grid(row=0,column=0, sticky="w")
        playback_frame = tk.Frame(self)
        playback_frame.grid(row=1,column=0)
        capture_frame = tk.Frame(self)
        capture_frame.grid(row=2,column=0)

        ssh_header = tk.Label(ssh_frame,text="Connect to DUT", font=("Arial", 16))
        ssh_header.grid(row=0, column=0)

        self.ip_entry = tk.Entry(ssh_frame)
        self.ip_entry.grid(row=1, column=0)

        self.user_entry = tk.Entry(ssh_frame)
        self.user_entry.insert(0, "test")
        self.user_entry.grid(row=2, column=0)

        self.password_entry = tk.Entry(ssh_frame, show="*")
        self.password_entry.insert(0, "test")
        self.password_entry.grid(row=3, column=0)

        connect_button = tk.Button(ssh_frame, text="Connect", command=self.connectThread)
        connect_button.grid(row=4, column=0)

        duration_label = tk.Label(self, text="Duration")
        duration_label.grid(row=0, column=0, sticky="ne", padx="130")

        self.duration_entry = tk.Entry(self)
        self.duration_entry.insert(0, "15")
        self.duration_entry.grid(row=0, column=0, sticky="ne")

        refresh_endpoints_button = tk.Button(self,text="Refresh Endpoints", command=self.getAudioDevices)
        refresh_endpoints_button.grid(row=0, column=0, sticky="ne", pady=20, padx=11)

        self.status_label = tk.Label(self, text="1")
        self.status_label.grid(row=0, column=0, sticky="ne", padx=11, pady=50)

        separator1 = ttk.Separator(ssh_frame, orient="horizontal")
        separator1.grid(row=5, column=0, columnspan=8, pady=10, sticky='ew')

        #PLAYBACK
        pb_header = tk.Label(playback_frame, text="Playback", font=("Arial", 16))
        pb_header.grid(row=0, column=0)

        pb_dev_label = tk.Label(playback_frame, text="Device")
        pb_dev_label.grid(row=1, column=0)

        self.pb_dev_entry = tk.Entry(playback_frame)
        self.pb_dev_entry.insert(0, "1,1")
        self.pb_dev_entry.grid(row=1, column=1)

        pb_channel_label = tk.Label(playback_frame, text="Channels")
        pb_channel_label.grid(row=1, column=2)

        self.pb_channel_entry = tk.Entry(playback_frame)
        self.pb_channel_entry.insert(0, "2")
        self.pb_channel_entry.grid(row=1, column=3)

        pb_format_label = tk.Label(playback_frame, text="Format")
        pb_format_label.grid(row=1, column=4)

        self.pb_format_entry = tk.Entry(playback_frame)
        self.pb_format_entry.insert(0, "S24_LE")
        self.pb_format_entry.grid(row=1, column=5)

        pb_freq_label = tk.Label(playback_frame, text="Frequency")
        pb_freq_label.grid(row=1, column=6)

        self.pb_freq_entry = tk.Entry(playback_frame)
        self.pb_freq_entry.insert(0, "48000")
        self.pb_freq_entry.grid(row=1, column=7)

        pb_file_label = tk.Label(playback_frame, text="Choose file to upload")
        pb_file_label.grid(row=2, column=0)

        self.pb_exec_button = tk.Button(playback_frame, text="Test", command=self.playbackThread)
        self.pb_exec_button.grid(row=2, column=7, sticky="e", padx=5)

        def browseFile():
            self.pb_file_entry = filedialog.askopenfilename()

        self.pb_file_button = tk.Button(playback_frame, text="Browse", command=browseFile)
        self.pb_file_button.grid(row=2, column=1)
        

        separator2 = ttk.Separator(playback_frame, orient="horizontal")
        separator2.grid(row=3, column=0, columnspan=8, pady=10, sticky='ew')

        #CAPTURE
        self.cp_header = tk.Label(capture_frame, text="Capture", font=("Arial", 16))
        self.cp_header.grid(row=0, column=0)

        self.cp_dev_label = tk.Label(capture_frame, text="Device")
        self.cp_dev_label.grid(row=1, column=0)

        self.cp_dev_entry = tk.Entry(capture_frame)
        self.cp_dev_entry.insert(0, "1,1")
        self.cp_dev_entry.grid(row=1, column=1)

        self.cp_channel_label = tk.Label(capture_frame, text="Channels")
        self.cp_channel_label.grid(row=1, column=2)

        self.cp_channel_entry = tk.Entry(capture_frame)
        self.cp_channel_entry.insert(0, "2")
        self.cp_channel_entry.grid(row=1, column=3)

        self.cp_format_label = tk.Label(capture_frame, text="Format")
        self.cp_format_label.grid(row=1, column=4)

        self.cp_format_entry = tk.Entry(capture_frame)
        self.cp_format_entry.insert(0, "S24_LE")
        self.cp_format_entry.grid(row=1, column=5)

        self.cp_freq_label = tk.Label(capture_frame, text="Frequency")
        self.cp_freq_label.grid(row=1, column=6)

        self.cp_freq_entry = tk.Entry(capture_frame)
        self.cp_freq_entry.insert(0, "48000")
        self.cp_freq_entry.grid(row=1, column=7)

        self.cp_file_label = tk.Label(capture_frame, text="Name file to download")
        self.cp_file_label.grid(row=2, column=0)

        self.cp_file_entry = tk.Entry(capture_frame)
        self.cp_file_entry.insert(0, "test.wav")
        self.cp_file_entry.grid(row=2, column=1)

        self.cp_exec_button = tk.Button(capture_frame, text="Test", command=self.captureThread)
        self.cp_exec_button.grid(row=2, column=7, sticky="e", padx=5)

        separator3 = ttk.Separator(capture_frame, orient="horizontal")
        separator3.grid(row=3, column=0, columnspan=8, pady=10, sticky='ew')

        self.text_area = tk.Text(self, bg="black", fg="white", wrap=tk.WORD)
        self.text_area.insert(tk.END, "Connect to DUT to show Audio endpoints \n\n 1. Playback \n\tRemember to turn on recording on controller\n\tSelect the file to upload and play on DUT, and press 'Test'\n\n 2. Capture\n\tRemember to play sine from controller to be recorded\n\tChoose the name of file that will be downloaded, and press 'Test'\n\nIMPORTANT!\nTry not to change connections because the cleanup for used files function only works on 1 connection per session\n\nOpen on local not on share. Permissions issues etc.")
        self.text_area.configure(state=tk.DISABLED)
        self.text_area.grid(row=3, column=0, sticky="nsew")
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.text_area2 = tk.Text(self, bg="black", fg="white", wrap=tk.WORD, height=1)
        self.text_area2.configure(state=tk.DISABLED)
        self.text_area2.grid(row=4, column=0, sticky="nsew")
        self.grid_rowconfigure(4, weight=0)
        self.grid_columnconfigure(0, weight=1)