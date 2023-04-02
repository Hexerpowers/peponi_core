import time
from threading import Thread

from Handler.Automatic.ManualHandler import ManualHandler
from Handler.Automatic.RuntimeHandler import RuntimeHandler


class MainHandler:
    def __init__(self, store):
        self.store = store
        self.store.lgm.init('Запускаю цикл подготовки...')
        self.store.get_rtm_store().set_val('running', True)
        self.handle = Thread(target=self.handle, daemon=True, args=())

    def handle(self):
        while True:
            time.sleep(1)
            print(self.store)

    def local_init(self):
        RuntimeHandler(self.store).start()
        ManualHandler(self.store).start()
        self.wait_init_check_pass('battery_ok')
        self.wait_init_check_pass('network_ok')
        self.wait_init_check_pass('integrity_ok')
        self.store.get_rtm_store().set_val('local_init_ok', True)
        self.handle.start()

    def wait_init_check_pass(self, name):
        self.store.lgm.init("Проверяю флаг: "+name)
        while not self.store.get_rtm_store().get_val(name):
            time.sleep(0.1)
