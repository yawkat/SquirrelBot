from module import Module

import urllib2
import json
import time
import traceback
import threading
import base64

class Jenkins(Module):
    def __init__(self, id, on, job, name, auth = ()):
        super(Jenkins, self).__init__(id)
        self.on = on
        self.job = job
        self.name = name
        self.auth = auth

        self.last_id = None

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
        url = self.job + "/api/json?depth=1"

        request = urllib2.Request(url)
        if len(self.auth) == 2:
            request.add_header("Authorization", "Basic " + base64.b64encode(self.auth[0] + ":" + self.auth[1]))
        stream = urllib2.urlopen(request)
        result = json.load(stream)

        last = result["lastCompletedBuild"]
        last_id = last["number"]

        if self.last_id and self.last_id != last_id:
            message = "Build " + self.name + "#" + str(last_id) + " completed [" + last["result"] + "]"
            self._broadcast(message)

        self.last_id = last_id

    def _broadcast(self, message):
        for name in self.on:
            if name in self.channels:
                self.channels[name].chat(message)