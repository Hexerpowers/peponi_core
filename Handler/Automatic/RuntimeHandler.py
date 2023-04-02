import time
from threading import Thread


class RuntimeHandler:
    def __init__(self, store):
        self.store = store
        self.handle = Thread(target=self.handle, daemon=True, args=())

    def start(self):
        self.handle.start()

    def handle(self):
        self.check_integrity()
        self.check_battery()
        self.check_network()
        while True:
            time.sleep(0.05)
            pass

    def check_battery(self):
        # TODO: сделать проверку состояния батареи
        self.store.get_rtm_store().set_val('battery_ok', True)

    def check_network(self):
        # TODO: сделать проверку адресов сети
        self.store.get_rtm_store().set_val('network_ok', True)

    def check_integrity(self):
        # TODO: сделать проверку целостности файлов
        self.store.get_rtm_store().set_val('integrity_ok', True)
