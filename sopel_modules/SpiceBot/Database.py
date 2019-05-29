# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Database
"""

# sopel imports
from sopel.tools import Identifier
from sopel.db import SopelDB

import threading
from .Config import config as botconfig


class BotDatabase():
    """A thread safe database cache"""

    def __init__(self):
        self.lock = threading.Lock()
        self.dict = {
                    "nicks": {},
                    "channels": {},
                    }
        self.db = SopelDB(botconfig.config)

    """Nick"""

    def get_nick_value(self, nick, key, sorting_key='unsorted'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = self.db.get_nick_id(nick, create=True)

        if nick_id not in self.dict["nicks"].keys():
            self.dict["nicks"][nick_id] = {}

        if sorting_key not in self.dict["nicks"][nick_id].keys():
            self.dict["nicks"][nick_id][sorting_key] = self.db.get_nick_value(nick, sorting_key) or dict()

        self.lock.release()

        if key not in self.dict["nicks"][nick_id][sorting_key].keys():
            return None
        else:
            return self.dict["nicks"][nick_id][sorting_key][key]

    def set_nick_value(self, nick, key, value, sorting_key='unsorted'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = self.db.get_nick_id(nick, create=True)

        if nick_id not in self.dict["nicks"].keys():
            self.dict["nicks"][nick_id] = {}

        if sorting_key not in self.dict["nicks"][nick_id].keys():
            self.dict["nicks"][nick_id][sorting_key] = self.db.get_nick_value(nick, sorting_key) or dict()

        self.dict["nicks"][nick_id][sorting_key][key] = value

        self.db.set_nick_value(nick, sorting_key, self.dict["nicks"][nick_id][sorting_key])

        self.lock.release()

    def delete_nick_value(self, nick, key, sorting_key='unsorted'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = self.db.get_nick_id(nick, create=True)

        if nick_id not in self.dict["nicks"].keys():
            self.dict["nicks"][nick_id] = {}

        if sorting_key not in self.dict["nicks"][nick_id].keys():
            self.dict["nicks"][nick_id][sorting_key] = self.db.get_nick_value(nick, sorting_key) or dict()

        del self.dict["nicks"][nick_id][sorting_key][key]
        self.db.set_nick_value(nick, sorting_key, self.dict["nicks"][nick_id][sorting_key])

        self.lock.release()

    def adjust_nick_value(self, nick, key, value, sorting_key='unsorted'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = self.db.get_nick_id(nick, create=True)

        if nick_id not in self.dict["nicks"].keys():
            self.dict["nicks"][nick_id] = {}

        if sorting_key not in self.dict["nicks"][nick_id].keys():
            self.dict["nicks"][nick_id][sorting_key] = self.db.get_nick_value(nick, sorting_key) or dict()

        if key not in self.dict["nicks"][nick_id][sorting_key].keys():
            oldvalue = []
        else:
            oldvalue = self.dict["nicks"][nick_id][sorting_key][key]

        if not oldvalue:
            self.dict["nicks"][nick_id][sorting_key][key] = value
        else:
            self.dict["nicks"][nick_id][sorting_key][key] = oldvalue + value
        self.db.set_nick_value(nick, sorting_key, self.dict["nicks"][nick_id][sorting_key])

        self.lock.release()

    def adjust_nick_list(self, nick, key, entries, adjustmentdirection, sorting_key='unsorted'):

        self.lock.acquire()

        if not isinstance(entries, list):
            entries = [entries]

        nick = Identifier(nick)
        nick_id = self.db.get_nick_id(nick, create=True)

        if nick_id not in self.dict["nicks"].keys():
            self.dict["nicks"][nick_id] = {}

        if sorting_key not in self.dict["nicks"][nick_id].keys():
            self.dict["nicks"][nick_id][sorting_key] = self.db.get_nick_value(nick, sorting_key) or dict()

        if key not in self.dict["nicks"][nick_id][sorting_key].keys():
            self.dict["nicks"][nick_id][sorting_key][key] = []

        if adjustmentdirection == 'add':
            for entry in entries:
                if entry not in self.dict["nicks"][nick_id][sorting_key][key]:
                    self.dict["nicks"][nick_id][sorting_key][key].append(entry)
        elif adjustmentdirection == 'del':
            for entry in entries:
                while entry in self.dict["nicks"][nick_id][sorting_key][key]:
                    self.dict["nicks"][nick_id][sorting_key][key].remove(entry)
        self.db.set_nick_value(nick, sorting_key, self.dict["nicks"][nick_id][sorting_key])

        self.lock.release()

    """Bot"""

    def get_bot_value(self, key, sorting_key='unsorted'):
        return self.get_nick_value(botconfig.nick, key, sorting_key)

    def set_bot_value(self, key, value, sorting_key='unsorted'):
        return self.set_nick_value(botconfig.nick, key, value, sorting_key)

    def delete_bot_value(self, key, sorting_key='unsorted'):
        return self.delete_nick_value(botconfig.nick, key, sorting_key)

    def adjust_bot_value(self, key, value, sorting_key='unsorted'):
        return self.adjust_nick_value(botconfig.nick, key, value, sorting_key)

    def adjust_bot_list(self, key, entries, adjustmentdirection, sorting_key):
        return self.adjust_nick_list(botconfig.nick, key, entries, adjustmentdirection, sorting_key)

    """Channels"""

    def get_channel_value(self, channel, key, sorting_key='unsorted'):

        self.lock.acquire()

        channel = Identifier(channel).lower().lower()

        if channel not in self.dict["channels"].keys():
            self.dict["channels"][channel] = {}

        if sorting_key not in self.dict["channels"][channel].keys():
            self.dict["channels"][channel][sorting_key] = self.db.get_channel_value(channel, sorting_key) or dict()

        self.lock.release()

        if key not in self.dict["channels"][channel][sorting_key].keys():
            return None
        else:
            return self.dict["channels"][channel][sorting_key][key]

    def set_channel_value(self, channel, key, value, sorting_key='unsorted'):

        self.lock.acquire()

        channel = Identifier(channel).lower()

        if channel not in self.dict["channels"].keys():
            self.dict["channels"][channel] = {}

        if sorting_key not in self.dict["channels"][channel].keys():
            self.dict["channels"][channel][sorting_key] = self.db.get_channel_value(channel, sorting_key) or dict()

        self.dict["channels"][channel][sorting_key][key] = value
        self.db.set_channel_value(channel, sorting_key, self.dict["channels"][channel][sorting_key])

        self.lock.release()

    def delete_channel_value(self, channel, key, sorting_key='unsorted'):

        self.lock.acquire()

        channel = Identifier(channel).lower()

        if channel not in self.dict["channels"].keys():
            self.dict["channels"][channel] = {}

        if sorting_key not in self.dict["channels"][channel].keys():
            self.dict["channels"][channel][sorting_key] = self.db.get_channel_value(channel, sorting_key) or dict()

        del self.dict["channels"][channel][sorting_key][key]
        self.db.set_channel_value(channel, sorting_key, self.dict["channels"][channel][sorting_key])

        self.lock.release()

    def adjust_channel_value(self, channel, key, value, sorting_key='unsorted'):

        self.lock.acquire()

        channel = Identifier(channel).lower()

        if channel not in self.dict["channels"].keys():
            self.dict["channels"][channel] = {}

        if sorting_key not in self.dict["channels"][channel].keys():
            self.dict["channels"][channel][sorting_key] = self.db.get_channel_value(channel, sorting_key) or dict()

        if key not in self.dict["channels"][channel][sorting_key].keys():
            oldvalue = None
        else:
            oldvalue = self.dict["channels"][channel][sorting_key][key]

        if not oldvalue:
            self.dict["channels"][channel][sorting_key][key] = value
        else:
            self.dict["channels"][channel][sorting_key][key] = oldvalue + value
        self.db.set_channel_value(channel, sorting_key, self.dict["channels"][channel][sorting_key])

        self.lock.release()

    def adjust_channel_list(self, channel, key, entries, adjustmentdirection, sorting_key='unsorted'):

        self.lock.acquire()

        if not isinstance(entries, list):
            entries = [entries]

        channel = Identifier(channel).lower()

        if channel not in self.dict["channels"].keys():
            self.dict["channels"][channel] = {}

        if sorting_key not in self.dict["channels"][channel].keys():
            self.dict["channels"][channel][sorting_key] = self.db.get_channel_value(channel, sorting_key) or dict()

        if key not in self.dict["channels"][channel][sorting_key].keys():
            self.dict["channels"][channel][sorting_key][key] = []

        if adjustmentdirection == 'add':
            for entry in entries:
                if entry not in self.dict["channels"][channel][sorting_key][key]:
                    self.dict["channels"][channel][sorting_key][key].append(entry)
        elif adjustmentdirection == 'del':
            for entry in entries:
                while entry in self.dict["channels"][channel][sorting_key][key]:
                    self.dict["channels"][channel][sorting_key][key].remove(entry)
        self.db.set_channel_value(channel, sorting_key, self.dict["channels"][channel][sorting_key])

        self.lock.release()

    """Plugins"""

    def get_plugin_value(self, plugin, key, sorting_key='unsorted'):

        self.lock.acquire()

        plugin = plugin.lower()

        if plugin not in self.dict["plugins"].keys():
            self.dict["plugins"][plugin] = {}

        if sorting_key not in self.dict["plugins"][plugin].keys():
            self.dict["plugins"][plugin][sorting_key] = self.db.get_plugin_value(plugin, sorting_key) or dict()

        self.lock.release()

        if key not in self.dict["plugins"][plugin][sorting_key].keys():
            return None
        else:
            return self.dict["plugins"][plugin][sorting_key][key]

    def set_plugin_value(self, plugin, key, value, sorting_key='unsorted'):

        self.lock.acquire()

        plugin = plugin.lower()

        if plugin not in self.dict["plugins"].keys():
            self.dict["plugins"][plugin] = {}

        if sorting_key not in self.dict["plugins"][plugin].keys():
            self.dict["plugins"][plugin][sorting_key] = self.db.get_plugin_value(plugin, sorting_key) or dict()

        self.dict["plugins"][plugin][sorting_key][key] = value
        self.db.set_plugin_value(plugin, sorting_key, self.dict["plugins"][plugin][sorting_key])

        self.lock.release()

    def delete_plugin_value(self, plugin, key, sorting_key='unsorted'):

        self.lock.acquire()

        plugin = plugin.lower()

        if plugin not in self.dict["plugins"].keys():
            self.dict["plugins"][plugin] = {}

        if sorting_key not in self.dict["plugins"][plugin].keys():
            self.dict["plugins"][plugin][sorting_key] = self.db.get_plugin_value(plugin, sorting_key) or dict()

        del self.dict["plugins"][plugin][sorting_key][key]
        self.db.set_plugin_value(plugin, sorting_key, self.dict["plugins"][plugin][sorting_key])

        self.lock.release()

    def adjust_plugin_value(self, plugin, key, value, sorting_key='unsorted'):

        self.lock.acquire()

        plugin = plugin.lower()

        if plugin not in self.dict["plugins"].keys():
            self.dict["plugins"][plugin] = {}

        if sorting_key not in self.dict["plugins"][plugin].keys():
            self.dict["plugins"][plugin][sorting_key] = self.db.get_plugin_value(plugin, sorting_key) or dict()

        if key not in self.dict["plugins"][plugin][sorting_key].keys():
            oldvalue = None
        else:
            oldvalue = self.dict["plugins"][plugin][sorting_key][key]

        if not oldvalue:
            self.dict["plugins"][plugin][sorting_key][key] = value
        else:
            self.dict["plugins"][plugin][sorting_key][key] = oldvalue + value
        self.db.set_plugin_value(plugin, sorting_key, self.dict["plugins"][plugin][sorting_key])

        self.lock.release()

    def adjust_plugin_list(self, plugin, key, entries, adjustmentdirection, sorting_key='unsorted'):

        self.lock.acquire()

        if not isinstance(entries, list):
            entries = [entries]

        plugin = plugin.lower()

        if plugin not in self.dict["plugins"].keys():
            self.dict["plugins"][plugin] = {}

        if sorting_key not in self.dict["plugins"][plugin].keys():
            self.dict["plugins"][plugin][sorting_key] = self.db.get_plugin_value(plugin, sorting_key) or dict()

        if key not in self.dict["plugins"][plugin][sorting_key].keys():
            self.dict["plugins"][plugin][sorting_key][key] = []

        if adjustmentdirection == 'add':
            for entry in entries:
                if entry not in self.dict["plugins"][plugin][sorting_key][key]:
                    self.dict["plugins"][plugin][sorting_key][key].append(entry)
        elif adjustmentdirection == 'del':
            for entry in entries:
                while entry in self.dict["plugins"][plugin][sorting_key][key]:
                    self.dict["plugins"][plugin][sorting_key][key].remove(entry)
        self.db.set_plugin_value(plugin, sorting_key, self.dict["plugins"][plugin][sorting_key])

        self.lock.release()


db = BotDatabase()
