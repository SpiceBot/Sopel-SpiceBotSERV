# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot

import spicemanip

# TODO custom gif shortcut commands


@SpiceBot.events.check_ready([SpiceBot.events.BOT_LOADED])
@SpiceBot.prerun('module')
@sopel.module.commands('gif')
def gif_trigger(bot, trigger, botcom):

    if not len(trigger.sb['args']):
        return SpiceBot.messagelog.messagelog_error(trigger.sb["log_id"], "Please present a query to search.")

    query = spicemanip.main(trigger.sb['args'], 0)
    searchapis = list(SpiceBot.gif.valid_api.keys())
    searchdict = {"query": query, "gifsearch": searchapis}

    gifdict = SpiceBot.gif.get_gif(searchdict)

    if gifdict["error"]:
        SpiceBot.messagelog.messagelog_error(trigger.sb["log_id"], gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))


@SpiceBot.prerun('module', "gif_prefix")
@sopel.module.commands('(.*)')
def gifapi_triggers(bot, trigger, botcom):

    if trigger.sb['com'] not in list(SpiceBot.gif.valid_api.keys()):
        return

    if not len(trigger.sb['args']):
        return SpiceBot.messagelog.messagelog_error(trigger.sb["log_id"], "Please present a query to search.")

    query = spicemanip.main(trigger.sb['args'], 0)
    searchdict = {"query": query, "gifsearch": trigger.sb['com']}

    gifdict = SpiceBot.gif.get_gif(searchdict)

    if gifdict["error"]:
        SpiceBot.messagelog.messagelog_error(trigger.sb["log_id"], gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))
