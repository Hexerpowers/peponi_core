import json
import time
from threading import Thread

import keyboard
import py_win_keyboard_layout
import requests
import win32api
import win32con


class KeyboardHandler:
    def __init__(self, st, lg):

        self.st = st
        self.lg = lg

        # Включаем английскую раскладку и NumLock
        py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)
        if self.is_num_lock_on() != 1:
            keyboard.press_and_release('num lock')

        self.x = 0
        self.y = 0

        self.upd_loop = Thread(target=self.update, daemon=True, args=())
        self.send_loop = Thread(target=self.send, daemon=True, args=())

    def start(self):
        self.upd_loop.start()
        self.send_loop.start()
        return self

    @staticmethod
    def is_num_lock_on():
        return win32api.GetKeyState(win32con.VK_NUMLOCK)

    def detect_key(self, e):
        if e.event_type == 'down' and e.name == 'up':
            self.x = 1
        if e.event_type == 'up' and e.name == 'up':
            self.x = 0

        if e.event_type == 'down' and e.name == 'down':
            self.x = -1
        if e.event_type == 'up' and e.name == 'down':
            self.x = 0

        if e.event_type == 'down' and e.name == 'left':
            self.y = 1
        if e.event_type == 'up' and e.name == 'left':
            self.y = 0

        if e.event_type == 'down' and e.name == 'right':
            self.y = -1
        if e.event_type == 'up' and e.name == 'right':
            self.y = 0

    def update(self):
        keyboard.hook_key('left', self.detect_key)
        keyboard.hook_key('right', self.detect_key)
        keyboard.hook_key('up', self.detect_key)
        keyboard.hook_key('down', self.detect_key)
        keyboard.wait()

    def send(self):
        while True:
            time.sleep(0.2)
            if self.st.get_manual():
                try:
                    req = requests.post('http://127.0.0.1:5252', data=json.dumps({"x": str(self.x), "y": str(self.y)}),
                                        timeout=0.5)
                except Exception as e:
                    pass
