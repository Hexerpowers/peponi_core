import subprocess as sp
from threading import Thread
from time import gmtime, strftime


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

    def run(self):
        while True:
            if self.st.get_record():
                if not self.running:
                    path = self.st.get_path().replace('|', '\\').replace('\\\\', '\\')
                    date = str(strftime("%Y-%m-%d_%H-%M-%S", gmtime()))
                    cmd = ['gst-launch-1.0', '-e', 'rtspsrc', "location=rtsp://192.168.88.110/live.sdp", '!', 'decodebin', '!',
                           'x264enc', '!', 'mp4mux', '!', 'filesink',
                           'location="'+path+'\platform_rec_' + date + '.mp4"']
                    self.vp = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
            else:
                if self.running:
                    self.vp.kill()
