import json
import time
from threading import Thread

import keyboard
import requests


class KeyboardHandler:
    def __init__(self, st, lg):

        self.st = st
        self.lg = lg

        self.x = 0
        self.y = 0
        self.yaw = 0
        self.cam_pitch = 0
        self.cam_zoom = 0

        self.current_cmd = {}
        self.prev_cmd = {}

        self.upd_loop = Thread(target=self.update, daemon=True, args=())
        self.send_loop = Thread(target=self.send, daemon=True, args=())

    def start(self):
        self.upd_loop.start()
        self.send_loop.start()
        return self

    def detect_key(self, e):
        if e.event_type == 'down' and e.name == 'n':
            self.cam_zoom = 1
        if e.event_type == 'up' and e.name == 'n':
            self.cam_zoom = 0

        if e.event_type == 'down' and e.name == 'm':
            self.cam_zoom = -1
        if e.event_type == 'up' and e.name == 'm':
            self.cam_zoom = 0

        if e.event_type == 'down' and e.name == 'o':
            self.cam_pitch = 1
        if e.event_type == 'up' and e.name == 'o':
            self.cam_pitch = 0

        if e.event_type == 'down' and e.name == 'l':
            self.cam_pitch = -1
        if e.event_type == 'up' and e.name == 'l':
            self.cam_pitch = 0

        if e.event_type == 'down' and e.name == ',':
            self.yaw = 1
        if e.event_type == 'up' and e.name == ',':
            self.yaw = 0

        if e.event_type == 'down' and e.name == '.':
            self.yaw = -1
        if e.event_type == 'up' and e.name == '.':
            self.yaw = 0

        if e.event_type == 'down' and e.name == 'up':
            self.x = 1
        if e.event_type == 'up' and e.name == 'up':
            self.x = 0

        if e.event_type == 'down' and e.name == 'down':
            self.x = -1
        if e.event_type == 'up' and e.name == 'down':
            self.x = 0

        if e.event_type == 'down' and e.name == 'left':
            self.y = -1
        if e.event_type == 'up' and e.name == 'left':
            self.y = 0

        if e.event_type == 'down' and e.name == 'right':
            self.y = 1
        if e.event_type == 'up' and e.name == 'right':
            self.y = 0

    def update(self):
        keyboard.hook_key('n', self.detect_key)
        keyboard.hook_key('m', self.detect_key)
        keyboard.hook_key('o', self.detect_key)
        keyboard.hook_key('l', self.detect_key)
        keyboard.hook_key('comma', self.detect_key)
        keyboard.hook_key('dot', self.detect_key)
        keyboard.hook_key('left', self.detect_key)
        keyboard.hook_key('right', self.detect_key)
        keyboard.hook_key('up', self.detect_key)
        keyboard.hook_key('down', self.detect_key)
        keyboard.wait()

    def send(self):
        while True:
            time.sleep(0.05)
            if self.st.get_manual():
                try:
                    self.current_cmd = {"x": str(self.x), "y": str(self.y), "yaw": str(self.yaw),
                                        "cam_pitch": str(self.cam_pitch), "cam_zoom": str(self.cam_zoom)}
                    if self.current_cmd != self.prev_cmd:
                        req = requests.post(
                            'http://' + self.st.config['network']['endpoint_addr'] + ':5052/api/v1/post/move',
                            data=json.dumps(self.current_cmd), timeout=2)
                        self.prev_cmd = self.current_cmd
                except Exception as e:
                    pass
