import os
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
            if self.st.get_record():
                if not self.running:
                    camera_address = self.st.config['network']['default_camera_address']
                    save_path = self.st.get_path().replace('|', '/')
                    date = str(strftime("%Y-%m-%d_%H-%M-%S", gmtime()))
                    script_path = os.path.dirname(os.path.abspath(__file__)) + '../../../Scripts/silent_start.vbs'
                    command_line = 'C:/gstreamer/1.0/msvc_x86_64/bin/gst-launch-1.0.exe -e rtspsrc ' \
                                   'location=rtsp://' + camera_address + \
                                   '/live.sdp ! decodebin ! x264enc ! mp4mux ! filesink' \
                                   ' location="' + save_path + '/platform_rec_' + date + '.mp4"'
                    cmd = ['cscript', script_path, command_line]
                    self.vp = sp.Popen(cmd, stdout=sp.PIPE)
                    self.running = True
            else:
                if self.running:
                    pid = self.find_process_pid('gst-launch-1.0.exe')
                    console_ctrl.send_ctrl_c(pid)
                    self.running = False
            time.sleep(0.5)
