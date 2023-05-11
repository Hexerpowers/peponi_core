class Store:
    def __init__(self, config):
        self.config = config

        self.power = {
            "state": 0,
            "voltage": 0,
            "current_0": 0,
            "current_1": 0
        }

        self.hank = {
            "state": 0,
            "direction": 0,
            "load": 0,
            "length": 0,
            "op_time": 0
        }

        self.hank_params = {
            "pull_force": 0,
            "free_length": 3,
            "target_length": 0

        }

        self.endpoint_addr = self.config['network']['default_endpoint_address']

        self.manual = False

        self.record = False

        self.path = "C:/Watchman/Camera"

    def toggle_manual(self):
        self.manual = not self.manual

    def toggle_record(self):
        self.record = not self.record

    def get_manual(self):
        return self.manual

    def get_power(self):
        return self.power

    def get_hank(self):
        return self.hank

    def get_path(self):
        return self.path

    def get_endpoint_addr(self):
        return self.endpoint_addr

    def get_record(self):
        return self.record

    def get_hank_params(self):
        return self.hank_params

    def set_power(self, power):
        self.power = power

    def set_hank(self, hank):
        self.hank = hank

    def set_path(self, path):
        self.path = path

    def set_endpoint_addr(self, addr):
        self.endpoint_addr = addr

    def set_hank_params(self, hank_params):
        self.hank_params = hank_params
