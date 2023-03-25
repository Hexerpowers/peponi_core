import random


class Store:
    def __init__(self, config):
        if config['general']['mode'] == 'sim':
            self.position = {
                'pos_x': random.randint(0, 12000),
                'pos_y': random.randint(0, 3000),
                'pos_t': random.randint(0, 360)
            }
        else:
            self.position = {
                'pos_x': 0,
                'pos_y': 0,
                'pos_t': 0
            }

        self.p_position = {
            'pos_x': 0,
            'pos_y': 0
        }

        self.pp_position = {
            'pos_x': 0,
            'pos_y': 0
        }

        self.telemetry = {
            "charge_level": 0,
            "signal_strength": 0,
        }

        self.runtime = {
            "route": {},
            "accuracy": 0
        }

    def __str__(self):
        return "Position: " + str(self.position) + "\nTelemetry: " + str(self.telemetry)

    def set_position(self, time, pos_x, pos_y):
        if time == 0:
            self.position['pos_x'] = int(pos_x)
            self.position['pos_y'] = int(pos_y)
        if time == 1:
            self.p_position['pos_x'] = int(pos_x)
            self.p_position['pos_y'] = int(pos_y)
        if time == 2:
            self.pp_position['pos_x'] = int(pos_x)
            self.pp_position['pos_y'] = int(pos_y)

    def set_theta(self, pos_t):
        self.position['pos_t'] = int(pos_t)

    def set_accuracy(self, accuracy):
        self.position['accuracy'] = int(accuracy)

    def set_telemetry(self, charge_level, signal_strength):
        self.telemetry['charge_level'] = int(charge_level)
        self.telemetry['signal_strength'] = int(signal_strength)

    def set_route(self, route):
        self.runtime['route'] = route

    def get_position(self, time):
        if time == 0:
            return self.position
        if time == 1:
            return self.p_position
        if time == 2:
            return self.pp_position

    def get_telemetry(self): return self.telemetry

    def get_runtime(self): return self.runtime
