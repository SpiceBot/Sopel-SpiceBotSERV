# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.rule(r"""(?:)u/
          (
            (?:\\/ | [^/])+
          )
          """)
@sopel.module.rule(r"""(?:)r/
          (
            (?:\\/ | [^/])+
          )
          """)
def bot_command_reddit_syntax(bot, trigger):
    message = SpiceBot.reddit.prerun(trigger)
    bot.osd(message)