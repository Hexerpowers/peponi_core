import json
import math
import socket
import time
from threading import Thread

import requests
from Modules.Common.Logger import Logger

from Modules.Store import Store

from Modules.Handler.KeyboardHandler import KeyboardHandler
from Modules.Handler.VideoHandler import VideoHandler


class Handler:
    def __init__(self, config, st: Store, lg: Logger):
        self.config = config
        self.st = st
        self.lg = lg

        self.hank_power_ok = 0
        self.hank_prev_target_length = 0

        self.hank_loop = Thread(target=self.hank, daemon=True, args=())
        self.power_loop = Thread(target=self.power, daemon=True, args=())

        self.remote_address = config['network']['default_hank_address']
        self.data_port = 700
        self.tx_thread = Thread(target=self.tx_void, daemon=True, args=())
        self.tx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = True
        self.lg.init('[TX] Подключаюсь к сокету: ' + str((self.remote_address, self.data_port)))
        try:
            self.tx_socket.connect((self.remote_address, self.data_port))
        except Exception as e:
            self.lg.error('[TX] Ошибка подключения к сокету: ' + str(e))
            self.ready = False

    def start(self):
        if self.ready:
            self.tx_thread.start()
            self.lg.log('[MX] Подключение к ' + str((self.remote_address, self.data_port)) + ': успешно.')
        self.power_loop.start()
        KeyboardHandler(self.st, self.lg).start()
        VideoHandler(self.st, self.lg).start()

    @staticmethod
    def calc_length_by_turns(turns):
        turns = float(turns)
        cable_diam = 0.08
        hank_width = 0.32
        hank_rad = 0.275 / 2
        layer = int((turns * cable_diam) / hank_width)
        if layer > 0:
            return round(((hank_width / cable_diam) * 2 * math.pi * (((turns * cable_diam) / hank_width - layer) * (
                    hank_rad + layer * cable_diam) + layer * hank_rad + cable_diam * (layer - 1))), 1)
        else:
            return round((2 * math.pi * hank_rad * turns), 1)

    @staticmethod
    def calc_turns_by_length(target_length):
        cable_diam = 0.08
        hank_rad = 0.275 / 2

        target_length = round(float(target_length))
        if target_length < 4:
            target_length = 4
        target_length = target_length + target_length * 0.04

        if 0 < target_length <= 25.918:
            return target_length / (2 * math.pi * hank_rad)

        if 25.918 < target_length <= 53.91:
            return (target_length - 25.918) / (2 * math.pi * (hank_rad + 2 * cable_diam)) + 30

        if 53.91 < target_length <= 83.97:
            return (target_length - 53.91) / (2 * math.pi * (hank_rad + 4 * cable_diam)) + 60

        if 83.97 <= target_length:
            return (target_length - 83.97) / (2 * math.pi * (hank_rad + 6 * cable_diam)) + 90

    @staticmethod
    def calc_load(raw_load):
        raw_load = int(raw_load)
        if raw_load < 0:
            return 0
        else:
            return round((raw_load / 100000), 1)

    def tx_void(self):
        while True:
            try:
                while True:
                    drop = "1" if self.st.get_drop() else "0"
                    self.tx_socket.sendall(json.dumps({'drop' : str(drop)}).encode('utf-8'))
                    data = self.tx_socket.recv(128)
                    print(data)
                    time.sleep(0.01)
                    if drop == "1":
                        self.st.set_drop(False)
            except Exception as e:
                self.lg.error('[TX] Ошибка подключения или передачи: ' + str(e))
            time.sleep(1)

    def hank(self):
        while True:
            time.sleep(0.5)
            try:
                if int(self.st.get_hank_params()['mode']) == 1:
                    hank_params = self.st.get_hank_params()
                    req = requests.get(
                        'http://' + self.config['network']['default_hank_address'] + "?pull_force=" + str(
                            10 + int(hank_params['pull_force'])) + "&free_length=" + str(
                            hank_params['free_length']) + "&",
                        timeout=2)
                    if req.status_code == 200:
                        raw_response = req.text
                        json_resp = json.loads(raw_response)
                        self.hank_power_ok = 1
                        self.st.set_hank({
                            "state": 1,
                            "direction": json_resp['direction'],
                            "load": self.calc_load(json_resp['load']),
                            "length": self.calc_length_by_turns(json_resp['turns']),
                            "op_time": json_resp['time'],
                        })

                elif int(self.st.get_hank_params()['mode']) == 2:
                    hank_params = self.st.get_hank_params()
                    target_length = round(self.calc_turns_by_length(hank_params['target_length']), 2)
                    req = requests.get(
                        'http://' + self.config['network']['default_hank_address'] + "?pull_force=" + str(
                            10 + int(hank_params['pull_force'])) + "&free_length=" + str(
                            hank_params['free_length']) + "&target_length=" + str(
                            target_length) + "&target_mode=" + str(hank_params['target_mode']) + "&target_alt=" + str(
                            hank_params['target_alt']) + "&",
                        timeout=3)
                    if req.status_code == 200:
                        raw_response = req.text
                        json_resp = json.loads(raw_response)
                        self.hank_power_ok = 1
                        self.st.set_hank({
                            "state": 1,
                            "direction": json_resp['direction'],
                            "load": self.calc_load(json_resp['load']),
                            "length": self.calc_length_by_turns(json_resp['turns']),
                            "op_time": json_resp['time'],
                        })
                else:
                    self.hank_power_ok = 0
                    self.st.set_hank({
                        "state": 0,
                        "direction": 0,
                        "load": 0,
                        "length": 0,
                        "op_time": 0
                    })

            except Exception:
                self.hank_power_ok = 0
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
                req = requests.get('http://' + self.st.get_endpoint_addr() + ':5052/api/v1/get/power', timeout=2)
                if req.status_code == 200:
                    raw_response = req.text
                    json_resp = json.loads(raw_response)
                    self.st.set_power({
                        "state": int(json_resp['state']),
                        "voltage": float(json_resp['voltage']),
                        "current_0": float(json_resp['current_0']),
                        "current_1": float(json_resp['current_1']),
                    })
            except Exception:
                self.st.set_power({
                    "state": int(self.hank_power_ok),
                    "voltage": 0,
                    "current_0": 0,
                    "current_1": 0
                })
