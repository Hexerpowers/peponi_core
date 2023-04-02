class RuntimeStore:
    def __init__(self, config, lgm):
        self.store = {
            "running": False,
            "battery_ok": False,
            "network_ok": False,
            "integrity_ok": False,

            "local_init_ok": False,
        }

    def get_full_val(self):
        return self.store

    def get_val(self, name):
        return self.store[name]

    def set_val(self, name, value):
        self.store[name] = value
