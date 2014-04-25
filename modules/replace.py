from module import Module

from irc_format import *

import re
import Queue

class Replace(Module):
    def __init__(self):
        super(Replace, self).__init__("replace")

        self.regex = re.compile("^[sS]/([^/]+)/([^/]+)/?$")
        self.history = []

    def on_chat(self, message):
        filtered = remove_colors(message.message)
        match = self.regex.match(filtered)
        if match:
            needle = match.group(1)
            print "Searching " + needle
            for item in reversed(self.history):
                print item.message
                if needle in item.message:
                    replacement = BOLD + match.group(2) + RESET
                    print "Replacing with " + replacement
                    message.channel.chat("Correction, <" + item.sender + "> " + remove_colors(item.message).replace(needle, replacement))
                    break
        else:
            self.history.append(message)
            if len(self.history) > 30:
                self.history = self.history[len(self.history)-30:]