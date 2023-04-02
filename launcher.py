import sys
import os
import time
import configparser

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from Common.LogManager import LogManager
from Store.MainStore import MainStore
from Handler.MainHandler import MainHandler

config = configparser.ConfigParser()
config.read("Assets/watchman_core.cfg")

lgm = LogManager(config)
lgm.init("Запускаюсь...")
m_store = MainStore(config, lgm)

MainHandler(m_store).local_init()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt as e:
    lgm.log('KeyboardInterrupt, остановлено пользователем')
    lgm.__del__()
