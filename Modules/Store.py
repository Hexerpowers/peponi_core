import random


class Store:
    def __init__(self, config):
        self.config = config

        self.power = {
            "state": 0,
            "voltage": 0,
            "current": 0
        }

        self.hank = {
            "state": 0,
            "direction": 0,
            "load": 0,
            "length": 0
        }

        self.manual = False

        self.path = "C:\Watchman\Camera"

    def toggle_manual(self):
        self.manual = not self.manual

    def get_manual(self):
        return self.manual

    def get_power(self):
        return self.power

    def get_hank(self):
        return self.hank

    def get_path(self):
        return self.path

    def set_power(self, power):
        self.power = power

    def set_hank(self, hank):
        self.hank = hank

    def set_path(self, path):
        self.path = path
