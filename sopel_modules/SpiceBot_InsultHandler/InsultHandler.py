# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.tools import stderr

import spicemanip

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs, command_permissions_check, inlist, inlist_match


def configure(config):
    pass


def setup(bot):
    pass


@sopel.module.rule(r'(?i)(Fuck|Screw) (you|off),? $nickname[ \t]*$')
def bot_command_srewyou(bot, trigger):
    bot.osd("Watch your mouth, " + trigger.nick + ", or I'll tell your mother!")


@sopel.module.rule(r'(?i)(Damnit|Lazy)? $nickname[ \t]*$')
def bot_command_damnlazy(bot, trigger):
    bot.osd("I do not tell you how to do your job, " + trigger.nick + "!!!")