from threading import Thread
import keyboard


class Keyboard:
    def __init__(self, store):
        self.store = store
        self.vals = []
        # TODO: Придумать схему управления с клавиатуры

        self.thread = Thread(target=self.update, daemon=True, args=())

    def get_vals(self):
        return self.vals

    def start(self):
        self.thread.start()
        return self

    def detect_key(self, e):
        if e.event_type == 'down' and e.name == '8':
            # do something
            pass

    def update(self):
        # keyboard.hook_key('some_key', self.detect_key)
        keyboard.wait()
