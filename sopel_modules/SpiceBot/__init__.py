# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
These are the core SpiceBot Classes

This module contains references only for other modules to utilize.
"""

from .Tools import *
from .Logs import *
from .Commands import *
from .Events import *
from .Channels import *
from .Database import *

__author__ = 'Sam Zick'
__email__ = 'sam@deathbybandaid.net'
__version__ = '0.1.1'


botdb = BotDatabase()
botchannels = BotChannels()
botcommands = BotCommands()
botevents = BotEvents()
botlogs = BotLogs()
