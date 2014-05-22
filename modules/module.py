import threading
import traceback
import time

class Module(object):
    def __init__(self, id):
        self.id = id
        self.channels = {}

    def on_chat(self, message):
        pass

    def init(self):
        pass

class StatusModule(Module):
    def __init__(self, id, on=[]):
        super(StatusModule, self).__init__(id)
        self.on = on

    def init(self):
        threading.Thread(target=self._repeated_poll).start()

    def _repeated_poll(self):
        i = 0
        while 1:
            try:
                self._poll_indexed(i)
            except:
                traceback.print_exc()
            time.sleep(5)
            i = i + 1

    def _poll_indexed(self, index):
        self._poll()

    def _poll(self):
        pass

    def _broadcast(self, message):
        for name in self.on:
            if name in self.channels:
                self.channels[name].chat(message)