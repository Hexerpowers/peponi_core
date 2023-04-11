import json
import time
from threading import Thread

import requests

from Modules.Handler.KeyboardHandler import KeyboardHandler
from Modules.Handler.VideoHandler import VideoHandler


class Handler:
    def __init__(self, config, st, lg):
        self.config = config
        self.st = st
        self.lg = lg
        self.hank_loop = Thread(target=self.hank, daemon=True, args=())
        self.power_loop = Thread(target=self.power, daemon=True, args=())

    def start(self):
        self.hank_loop.start()
        self.power_loop.start()
        KeyboardHandler(self.st, self.lg).start()
        # VideoHandler(self.st, self.lg).start()

    @staticmethod
    def calc_length(turns):
        return 68

    def hank(self):
        while True:
            time.sleep(1)
            try:
                req = requests.get('http://'+self.config['network']['hank_addr'], timeout=3)
                if req.status_code == 200:
                    raw_response = req.text
                    json_resp = json.loads(raw_response)
                    self.st.set_hank({
                        "state": 1,
                        "direction": json_resp['direction'],
                        "load": json_resp['load'],
                        "length": self.calc_length(json_resp['turns']),
                        "op_time": json_resp['op_time'],
                    })
                    self.st.set_power(json_resp['power'])
            except Exception as e:
                self.st.set_hank({
                    "state": 0,
                    "direction": 0,
                    "load": 0,
                    "length": 0,
                    "op_time": 0
                })

    def power(self):
        while True:
            time.sleep(0.5)
            try:
                req = requests.get('http://'+self.st.get_endp_addr()+':5052/api/v1/get/power', timeout=1)
                if req.status_code == 200:
                    raw_response = req.text
                    json_resp = json.loads(raw_response)
                    self.st.set_power({
                        "state": json_resp['state'],
                        "voltage": json_resp['voltage'],
                        "current": json_resp['current'],
                    })
            except Exception as e:
                self.st.set_power({
                    "state": 1,
                    "voltage": 0,
                    "current": 0,
                })
