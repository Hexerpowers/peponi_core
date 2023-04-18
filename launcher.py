import configparser
import os
import time
import subprocess as sp

import console_ctrl
import psutil

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

script_path = os.path.dirname(os.path.abspath(__file__)) + '/Scripts/silent_start.vbs'
command_line = os.path.dirname(os.path.abspath(__file__)) + '/Scripts/go2rtc.exe'
cmd = ['cscript', script_path, command_line]

NW.wait_for_connection()

HD.start()
TR.start()

sp.Popen(cmd, stdout=sp.PIPE)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt as e:
    LG.log('KeyboardInterrupt, остановлено пользователем')
    pid = 0
    for process in psutil.process_iter():
        if process.name() == 'go2rtc.exe':
            pid = process.pid
    console_ctrl.send_ctrl_c(pid)
