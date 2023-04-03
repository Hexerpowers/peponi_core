import configparser
import time

from Modules.Handler.MainHandler import Handler
from Modules.Common.Logger import Logger
from Modules.Common.Network import Network
from Modules.Store import Store
from Modules.HttpServer import HttpServer

config = configparser.ConfigParser()
config.read("core.cfg")

LG = Logger(config)
ST = Store(config)
HD = Handler(config, ST, LG)
TR = HttpServer(config, ST, LG)
NW = Network(config, ST, LG)

NW.wait_for_connection()

HD.start()
TR.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt as e:
    LG.log('KeyboardInterrupt, остановлено пользователем')
