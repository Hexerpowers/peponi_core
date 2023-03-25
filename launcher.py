import configparser
import time
import pythonping

from Modules.Handler import Handler
from Modules.Logger import Logger
from Modules.Network import Network
from Modules.Store import Store
from Modules.Transport import Transport

config = configparser.ConfigParser()
config.read("core.cfg")

LG = Logger()
ST = Store()
HD = Handler(config, ST, LG)
TR = Transport(config, ST, LG)
NW = Network(config, ST, LG)

# NW.wait_for_connection()
NW.ping_inet()
boot_lock = NW.ping_server()

if boot_lock or config['general']['mode'] == 'test':
    HD.start()
    TR.start()

    while True:
        time.sleep(1)
