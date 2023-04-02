from threading import Thread


class ShutdownHandler:
    def __init__(self):
        self.handle = Thread(target=self.handle, daemon=True, args=())

    def start(self):
        self.handle.start()

    def handle(self):
        pass
