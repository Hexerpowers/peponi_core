import random


class Store:
    def __init__(self, config):
        if config['general']['mode'] == 'sim':
            self.position = {
                'pos_x': random.randint(0, 12000),
                'pos_y': random.randint(0, 3000),
                'pos_t': random.randint(0, 360),
                'accuracy': 0,
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

        if config['general']['mode'] == 'sim':
            self.runtime = {
                "state": False,
                "route": {
                    "repeat": True,
                    "waypoints": [[1000, 2000], [5000, 2000]]
                },
                "accuracy": 0
            }
        else:
            self.runtime = {
                "state": False,
                "route": {}
            }

        self.tracking = {
            "position_timestamp": 0,
            "robot_timestamp": 0,
            "position_ok": False,
            "robot_ok": False
        }

    def __str__(self):
        return "Position: " + str(self.position)

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

    def set_route(self, route):
        self.runtime['route'] = route

    def set_state(self, state):
        self.runtime['state'] = bool(state)

    def set_position_timestamp(self, timestamp):
        self.tracking['position_timestamp'] = timestamp

    def set_robot_timestamp(self, timestamp):
        self.tracking['robot_timestamp'] = timestamp

    def set_tracking_ok(self, position_ok, robot_ok):
        self.tracking['position_ok'] = position_ok
        self.tracking['robot_ok'] = robot_ok

    def get_tracking(self):
        return self.tracking

    def get_position(self, time):
        if time == 0:
            return self.position
        if time == 1:
            return self.p_position
        if time == 2:
            return self.pp_position

    def get_runtime(self):
        return self.runtime
