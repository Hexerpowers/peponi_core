import socket
import time
from threading import Thread

import pythonping
from netifaces import interfaces, ifaddresses, AF_INET

from Modules.Common.Logger import Logger
from Modules.Store import Store


class Network:
    def __init__(self, config, st: Store, lg: Logger):
        self.config = config
        self.st = st
        self.lg = lg

        self.found_shown = False

        self.rpi_hostname_loop = Thread(target=self.update_rpi_hostname, daemon=True, args=())

    def update_rpi_hostname(self):
        hostname = self.config['network']['default_endpoint_address']
        while True:
            time.sleep(0.8)
            try:
                if not self.found_shown:
                    hostname = socket.gethostbyname(self.config['network']['default_endpoint_hostname'])
                    if not self.found_shown:
                        self.lg.log("Найден коптер по адресу: %s" % hostname)
                        self.found_shown = True
                else:
                    response_list = pythonping.ping(self.st.get_endpoint_addr(), size=20, count=2,
                                                    timeout=2)
                    if int(response_list.rtt_avg_ms) > 200:
                        self.found_shown = False
            except Exception as e:
                print(e)
                hostname = self.config['network']['default_endpoint_address']
                self.found_shown = False

            self.st.set_endpoint_addr(hostname)

    def start(self):
        self.rpi_hostname_loop.start()
        return self

    def wait_for_connection(self):
        subnets = str(self.config['network']['working_subnets']). \
            replace(' ', '').replace('[', '').replace(']', '').split(',')
        local_addresses = []
        for subnet in subnets:
            self.lg.init("Ожидание подключения с подсетью " + subnet + "...")
        net_available = False
        while not net_available:
            for ifaceName in interfaces():
                addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
                for addr in addresses:
                    for subnet in subnets:
                        if subnet in addr:
                            local_addresses.append(addr)
            if len(local_addresses) > 0:
                net_available = True
                for addr in local_addresses:
                    self.lg.init("Сетевое подключение [" + str(addr) + "] обнаружено.")
            time.sleep(1)
