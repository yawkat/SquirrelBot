from module import Module

from irc_format import *

import re
import Queue

class Replace(Module):
    def __init__(self):
        super(Replace, self).__init__("replace")

        self.regex = re.compile("^[sS]([^\w\s])(((?!\\1).)*)\\1(((?!\\1).)*)(\\1(((?!\\1).)*))?$")
        self.history = []

    def on_chat(self, message):
        filtered = remove_colors(message.message)
        match = self.regex.match(filtered)
        if match:
            args = (match.group(2), match.group(4), match.group(7))
            print str(match.groups()) + " " + str(args)
            try:
                needle = re.compile(args[0])
            except:
                needle = re.compile(re.escape(args[0]))
            flag = args[2]
            for item in reversed(self.history):
                if flag and flag != 'g' and not flag in item.sender:
                    continue

                print item.message
                if needle.search(item.message) is not None:
                    replacement = BOLD + args[1] + RESET

                    count = 1
                    if flag == 'g':
                        count = 0
                    try:
                        corrected = needle.sub(replacement, remove_colors(item.message), count=count)
                    except:
                        corrected = needle.sub(re.escape(replacement), remove_colors(item.message), count=count)
                    message.channel.chat("Correction, <" + item.sender + "> " + corrected)
                    break
        else:
            self.history.append(message)
            if len(self.history) > 30:
                self.history = self.history[len(self.history)-30:]