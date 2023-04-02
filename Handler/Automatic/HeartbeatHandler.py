from threading import Thread


class HeartbeatHandler:
    def __init__(self):
        self.handle = Thread(target=self.handle, daemon=True, args=())

    def start(self):
        self.handle.start()

    def handle(self):
        pass
