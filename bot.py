#!/usr/bin/env python

import api
import config

all_channels = {}

def after_connect(con, channels):
    for channel_info in channels:
        chan = con.join(channel_info["name"], lambda channel: channel.add_chat_listener(lambda message, nick=con.nick: on_chat(message, nick)), channel_info.get("key", ""))
        all_channels[con.host + "/" + chan.name] = chan
        all_channels[con.host + ":" + str(con.port) + "/" + chan.name] = chan

def on_chat(message, own_name):
    if not message.sender == own_name:
        print "Received " + str(message)
        for module in config.used_modules:
            module.on_chat(message)

for server in config.servers:
    connection = api.Connection(server["nick"], server["host"], server["port"])
    connection.connect(lambda con, channels = server["channels"]: after_connect(con, channels))

for module in config.used_modules:
    module.channels = all_channels
    module.init()