import subprocess as sp
import time
from threading import Thread
from time import gmtime, strftime

import console_ctrl
import psutil


class VideoHandler:
    def __init__(self, st, lg):
        self.st = st
        self.lg = lg
        self.running = False
        self.video_loop = Thread(target=self.run, daemon=True, args=())
        self.vp = None

    def start(self):
        self.video_loop.start()
        return self

    @staticmethod
    def find_process_pid(process_name):
        for process in psutil.process_iter():
            if process.name() == process_name:
                return process.pid

    def run(self):
        while True:
            # rtsp://192.168.88.110/live.sdp
            if self.st.get_record():
                if not self.running:
                    path = self.st.get_path().replace('|', '/')
                    date = str(strftime("%Y-%m-%d_%H-%M-%S", gmtime()))
                    command_line = 'C:/gstreamer/1.0/msvc_x86_64/bin/gst-launch-1.0.exe -e videotestsrc ! videoconvert ! videoscale ! video/x-raw,width=400,height=300 ! x264enc ! mp4mux ! filesink location="' + path + '/platform_rec_' + date + '.mp4"'
                    cmd = ['cscript', 'D:/Projects/Omega/Watchman/watchman_core/Scripts/silent_start.vbs', command_line]
                    self.vp = sp.Popen(cmd, stdout=sp.PIPE)
                    self.running = True
            else:
                if self.running:
                    pid = self.find_process_pid('gst-launch-1.0.exe')
                    console_ctrl.send_ctrl_c(pid)
                    self.running = False
            time.sleep(0.1)
