import configparser
import time

import pythonping

from Modules.Handler import Handler
from Modules.Logger import Logger
from Modules.Store import Store
from Modules.Transport import Transport

config = configparser.ConfigParser()
config.read("core.cfg")

LG = Logger()
ST = Store()
HD = Handler(config, ST, LG)
TR = Transport(config, ST, LG)

boot_lock = True
#
# try:
#     response_list = pythonping.ping('8.8.8.8', size=10, count=2, timeout=2)
#     ping = response_list.rtt_avg_ms
#     if ping < 2000:
#         LG.log("Пинг до Google (наличие сети): "+str(ping)+" ms")
#         boot_lock = True
#     else:
#         LG.err("Ошибка подключения к сети: превышено время ожидания (2000ms).")
#         boot_lock = False
# except Exception as e:
#     LG.err("Ошибка обнаружения сети: "+str(e))
#     boot_lock = False
#
# if boot_lock:
#     try:
#         response_list = pythonping.ping(config['network']['base_url'], size=10, count=2, timeout=2)
#         ping = response_list.rtt_avg_ms
#         if ping < 2000:
#             LG.log("Пинг до серверов Navigine: "+str(ping)+" ms")
#             boot_lock = True
#         else:
#             LG.err("Ошибка подключения к серверам Navigine: превышено время ожидания (2000ms).")
#             boot_lock = False
#     except Exception as e:
#         LG.err("Ошибка подключения к серверам Navigine: "+str(e))

if boot_lock:
    HD.start()
    TR.start()

    while True:
        time.sleep(1)
        #print(ST)

