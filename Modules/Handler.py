import math
import time
from threading import Thread


class Handler:
    def __init__(self, config, st, lg):
        self.config = config
        self.st = st
        self.lg = lg
        self.position_loop = Thread(target=self.position, daemon=True, args=())

    def start(self):
        self.position_loop.start()

    def position(self):
        while True:
            time.sleep(0.2)
            pos = self.st.get_position(0)
            p_pos = self.st.get_position(1)
            pp_pos = self.st.get_position(2)

            acc_x = abs(pos['pos_x']-(pos['pos_x']+p_pos['pos_x']+pp_pos['pos_x'])/3)
            acc_y = abs(pos['pos_y']-(pos['pos_y']+p_pos['pos_y']+pp_pos['pos_y'])/3)

            self.st.set_accuracy(max(acc_x, acc_y))

            position_ok = False
            robot_ok = False
            tracking = self.st.get_tracking()
            if math.floor(time.time()) - tracking['position_timestamp'] < 3:
                position_ok = True
            if math.floor(time.time()) - tracking['robot_timestamp'] < 3:
                robot_ok = True

            self.st.set_tracking_ok(position_ok, robot_ok)


