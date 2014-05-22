import module
from module import Module

from irc_format import *

class GitModule(module.StatusModule):
    def __init__(self, id, on, name):
        super(GitModule, self).__init__(id, on)
        self.name = name
        self.known = set()
        self.first = True

    def _poll_indexed(self, i):
        self.first = i == 0
        super(GitModule, self)._poll_indexed(i)

    def _commit(self, id, description, author):
        if not id in self.known:
            self.known.add(id)
            if not self.first: # on first run ignore all previous commits
                self._broadcast(BOLD + author + RESET + " pushed to " + self.name + ": " + description)