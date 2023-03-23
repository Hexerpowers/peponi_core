class Store:
    def __init__(self):
        self.position = {
            'pos_x': 0,
            'pos_y': 0,
            'pos_a': 0,
            'accuracy': 0,
        }

        self.telemetry = {
            "charge_level": 0,
            "signal_strength": 0,
        }

        self.params = {
            "field_width": 0,
            "field_height": 0,
            "offset_x": 0,
            "offset_y": 0,
            "magic_x": 0,
            "magic_y": 0,

            "client": "192.168.1.1"
        }

    def __str__(self):
        return "Position: " + str(self.position) + "\nTelemetry: " + str(self.telemetry) + "\nParams: " + str(
            self.params)

    def set_position(self, pos_x, pos_y):
        self.position['pos_x'] = int(pos_x)
        self.position['pos_y'] = int(pos_y)

    def set_angle(self, pos_a):
        self.position['pos_a'] = int(pos_a)

    def get_position(self):
        return self.position

    def set_accuracy(self, accuracy):
        self.position['accuracy'] = int(accuracy)

    def get_accuracy(self): return self.position['accuracy']

    def set_telemetry(self, charge_level, signal_strength):
        self.telemetry['charge_level'] = int(charge_level)
        self.telemetry['signal_strength'] = int(signal_strength)

    def get_telemetry(self): return self.telemetry

    def set_dimens(self, field_width, field_height, offset_x, offset_y, magic_x, magic_y):
        self.params['field_width'] = int(field_width)
        self.params['field_height'] = int(field_height)
        self.params['offset_x'] = float(offset_x)
        self.params['offset_y'] = float(offset_y)
        self.params['magic_x'] = float(magic_x)
        self.params['magic_y'] = float(magic_y)

    def set_credentials(self, client):
        self.params['client'] = client

    def get_params(self): return self.params
