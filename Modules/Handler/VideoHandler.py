import subprocess as sp
import time
from time import gmtime, strftime


class VideoHandler():
    def __init__(self, st, lg):
        self.st = st
        self.lg = lg

    def start(self):
        date = str(strftime("%Y-%m-%d_%H-%M-%S", gmtime()))
        cmd = ['gst-launch-1.0', '-e', 'rtspsrc', "location=rtsp://192.168.88.110/live.sdp", '!', 'decodebin', '!',
               'x264enc', '!', 'mp4mux', '!', 'filesink',
               'location="platform_rec_' + date + '.mp4"']
        sp.Popen(
            cmd,
            shell=True, stdout=sp.PIPE)
        return self
