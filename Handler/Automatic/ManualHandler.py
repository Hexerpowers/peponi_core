import time
from threading import Thread

from Handler.Hardware.Controller import Controller
from Handler.Hardware.Keyboard import Keyboard

from Common.ConstStorage import ConstStorage as CS


class ManualHandler:
    def __init__(self, store):
        self.store = store
        self.handle = Thread(target=self.handle, daemon=True, args=())

    def start(self):
        self.handle.start()

    def handle(self):
        self.store.lgm.init("Запускаю обработчик ввода")
        time.sleep(0.5)
        controller = Controller(self.store).start()
        keyboard = Keyboard(self.store).start()
        while True:
            time.sleep(0.01)
            cnt_vals = controller.get_vals()
            self.store.get_cmd_store().set_full_val(cnt_vals)
            if cnt_vals[4] > CS.MIN_VAL:
                self.store.get_rtm_store().set_val("copter_armed", True)
            else:
                self.store.get_rtm_store().set_val("copter_armed", False)

            if cnt_vals[6] < CS.MID_VAL:
                self.store.get_rtm_store().set_val("copter_mode", 0)
            elif cnt_vals[6] == CS.MID_VAL:
                self.store.get_rtm_store().set_val("copter_mode", 1)
            else:
                self.store.get_rtm_store().set_val("copter_mode", 2)

            # TODO: обработка клавиатуры
