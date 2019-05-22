# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.botevents.BOT_WELCOME)
@sopel.module.rule('.*')
def bot_events_connected(bot, trigger):
    """For items tossed in a queue, this will trigger them accordingly"""
    while True:
        if len(SpiceBot.botevents.SpiceBot_Events["trigger_queue"]):
            pretriggerdict = SpiceBot.botevents.SpiceBot_Events["trigger_queue"][0]
            SpiceBot.botevents.dispatch(bot, pretriggerdict)
            del SpiceBot.botevents.SpiceBot_Events["trigger_queue"][0]
