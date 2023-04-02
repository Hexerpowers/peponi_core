class HeartbeatStore:
    def __init__(self, config, lgm):
        self.store = {

        }

    def get_full_val(self):
        return self.store

    def get_val(self, name):
        return self.store[name]

    def set_val(self, name, value):
        self.store[name] = value
