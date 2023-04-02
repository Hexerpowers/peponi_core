class CommandStore:
    def __init__(self, config, lgm):
        self.store = []

    def get_full_val(self):
        return self.store

    def set_full_val(self, value):
        self.store = value
