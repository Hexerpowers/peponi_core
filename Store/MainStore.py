from Store.CommandStore import CommandStore
from Store.HeartbeatStore import HeartbeatStore
from Store.MessageStore import MessageStore
from Store.RuntimeStore import RuntimeStore


class MainStore:

    def __init__(self, config, lgm):
        self.config = config
        self.lgm = lgm
        self.command_store = CommandStore(config, lgm)
        self.heartbeat_store = HeartbeatStore(config, lgm)
        self.message_store = MessageStore(config, lgm)
        self.runtime_store = RuntimeStore(config, lgm)
        lgm.init('Хранилище инициализировано')

    def __str__(self):
        return f'''
        CommandStore:{self.command_store.get_full_val()}\r
        HeartbeatStore:{self.heartbeat_store.get_full_val()}\r
        MessageStore:{self.message_store.get_full_val()}\r
        RuntimeStore:{self.runtime_store.get_full_val()}\r
        '''

    def get_cmd_store(self):
        return self.command_store

    def get_hbt_store(self):
        return self.heartbeat_store

    def get_msg_store(self):
        return self.message_store

    def get_rtm_store(self):
        return self.runtime_store
