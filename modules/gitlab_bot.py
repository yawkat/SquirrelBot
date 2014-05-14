from module import Module

from irc_format import *

import gitlab
import threading
import traceback
import time
import irc_format

class Gitlab(Module):
    def __init__(self, id, on, url, name, project, auth = None):
        super(Gitlab, self).__init__(id)
        self.on = on
        self.name = name
        self.project = project

        self.git = gitlab.Gitlab(url, token=auth)
        self.known = None

    def init(self):
        threading.Thread(target=self._repeated_poll).start()

    def _repeated_poll(self):
        while 1:
            try:
                self._poll()
            except:
                traceback.print_exc()
            time.sleep(5)

    def _poll(self):
        first = self.known is None
        if first:
            self.known = set()
        commits = self.git.listrepositorycommits(self.project)
        commits.reverse()
        for commit in commits:
            if not commit["id"] in self.known:
                if not first:
                    self._broadcast(BOLD + commit["author_name"] + RESET + " pushed to " + self.name + ": " + commit["title"])
                self.known.add(commit["id"])

    def _broadcast(self, message):
        for name in self.on:
            if name in self.channels:
                self.channels[name].chat(message)