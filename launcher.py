import configparser
import os
import subprocess as sp
import time

from Modules.Common.Logger import Logger
from Modules.Common.Network import Network
from Modules.Handler.MainHandler import Handler
from Modules.HttpServer import HttpServer
from Modules.Store import Store

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "/core.cfg")

LG = Logger(config)
ST = Store(config)
HD = Handler(config, ST, LG)
TR = HttpServer(config, ST, LG)
NW = Network(config, ST, LG)

script_path = os.path.dirname(os.path.abspath(__file__)) + '/Scripts/silent_start.vbs'
command_line = os.path.dirname(
    os.path.abspath(__file__)) + '/Scripts/go2rtc.exe -config C:/Users/Watchman/watchman_core/Scripts/go2rtc.yaml'
cmd = ['cscript', script_path, command_line]

NW.wait_for_connection()

NW.start()

TR.start()
sp.Popen(cmd, stdout=sp.PIPE)
HD.start()

try:
    while True:
        time.sleep(1)
        running = True
except KeyboardInterrupt:
    LG.log('KeyboardInterrupt, остановлено пользователем')
    LG.__del__()
