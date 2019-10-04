# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function

# sopel imports
import sopel.module

from sopel_modules.spicemanip import spicemanip

import sopel_modules.SpiceBot as SpiceBot

import re
import requests
import bleach
from lxml import etree

from lxml import html

api_url = 'https://httpstatuses.com/'


@SpiceBot.prerun('module')
@sopel.module.commands('httpcode')
def bot_command_http_codes(bot, trigger, botcom):

    query = spicemanip(botcom.dict["args"], 1) or None
    if not query:
        return bot.osd("You must provide a HTTP status code to look up.")
    result = fetch_result(str(query))

    bot.osd(["[HTTP code search for " + str(query) + "]", result])


def fetch_result(query):

    if not re.match('^[1-5]\d{2}$', query):
        return "Invalid HTTP status code: %s" % query
    url = api_url + query
    try:
        r = requests.get(url=url, timeout=(10.0, 4.0))
    except requests.exceptions.ConnectTimeout:
        return "Connection timed out."
    except requests.exceptions.ConnectionError:
        return "Couldn't connect to server."
    except requests.exceptions.ReadTimeout:
        return "Server took too long to send data."
    if r.status_code == 404:
        return "Unknown HTTP status code: %s" % query
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return "HTTP error: " + e.message

    tree = html.fromstring(r.content)

    try:
        title = tree.xpath(('/html/body/article/p[1]')[0])
        # if isinstance(title, list):
        #    title = title[0]
        # title = str(title)
        # for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
        #    title = title.replace(*r)
        # title = unicode_string_cleanup(title)
    except Exception as e:
        title = None
    if title:
        return title
    else:
        return "An Error Occured"

    return

    page = etree.HTML(r.content)
    title = bleach.clean(etree.tostring(page.xpath('/html/body/article/h1[1]')[0]), tags=[], strip=True)
    summary = bleach.clean(
        re.sub('<a href="#ref-\d+">.*?<\/a>', '', etree.tostring(page.xpath('/html/body/article/p[1]')[0])), tags=[],
        strip=True)
    return "{title}: {summary} — {link}".format(title=title, summary=summary, link=url)
