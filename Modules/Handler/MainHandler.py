import json
import math
import socket
import time
from threading import Thread

import pythonping
import requests

from Modules.Common.Logger import Logger
from Modules.Handler.KeyboardHandler import KeyboardHandler
from Modules.Store import Store


class Handler:
    def __init__(self, config, st: Store, lg: Logger):
        self.config = config
        self.st = st
        self.lg = lg

        self.hank_power_ok = 0
        self.hank_prev_target_length = 0

    def start(self):
        KeyboardHandler(self.st, self.lg).start()
