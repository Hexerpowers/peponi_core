import json
import time
from threading import Thread
import requests


class Handler:
    def __init__(self, config, st, lg):
        self.config = config
        self.st = st
        self.lg = lg
        self.position_loop = Thread(target=self.position, daemon=True, args=())

    def start(self):
        self.position_loop.start()

    def position(self):
        got_once = False
        raw_response = ''
        parsed_response = json.loads("{}")
        if self.config['general']['mode'] == 'test':
            full_url = self.config['network']['protocol'] + self.config['network']['base_url'] + self.config['network'][
                'method'] + self.config['network']['test_args'] + self.config['network']['api_key']
        else:
            full_url = self.config['network']['protocol'] + self.config['network']['base_url'] + self.config['network'][
                'method'] + self.config['network']['args'] + self.config['network']['api_key']

        req_interval = float(self.config['general']['req_interval'])
        self.st.set_dimens(self.config['field']['initial_width'], self.config['field']['initial_height'],
                           self.config['field']['offset_x'], self.config['field']['offset_y'],
                           self.config['field']['magic_x'], self.config['field']['magic_y'])
        while True:
            time.sleep(req_interval)
            dimens = self.st.get_params()
            try:
                req = requests.get(full_url)
                if req.status_code == 200:
                    raw_response = req.text
                parsed_response = json.loads(raw_response)
                got_once = True
            except Exception as e:
                self.lg.err("Ошибка подключения к серверам Navigine: " + str(e))

            if got_once:
                try:
                    kx = (parsed_response['data'][0]['attributes']['kx'] - dimens['offset_x']) * dimens['magic_x']
                    if kx > dimens['field_width']:
                        kx = dimens['field_width']
                    if kx < 0:
                        kx = 0
                    ky = (parsed_response['data'][0]['attributes']['ky'] - dimens['offset_y']) * dimens['magic_y']
                    if ky > dimens['field_height']:
                        ky = dimens['field_height']
                    if ky < 0:
                        ky = 0

                    self.st.set_position(kx, ky)
                except Exception as e:
                    if str(e) == "list index out of range":
                        self.lg.err(
                            "Ошибка получения информации о метке: Ни одной активной метки за последние 30 минут.")
                    else:
                        self.lg.err("Ошибка получения информации о метке: " + str(e))
