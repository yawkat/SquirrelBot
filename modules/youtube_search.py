from module import Module
from irc_format import *

import urllib
import urllib2
import json
import time
import traceback
import threading

class YoutubeSearch(Module):
    def __init__(self, id, api_key, channels, search_term):
        super(YoutubeSearch, self).__init__(id)
        self.api_key = api_key
        self.channels = channels
        self.search_term = search_term

        self.last_upload_time = None

    def init(self):
        threading.Thread(target=self._repeated_poll).start()

    def _repeated_poll(self):
        while 1:
            try:
                self._poll()
            except:
                traceback.print_exc()
            time.sleep(20)

    def _poll(self):
        url = "https://www.googleapis.com/youtube/v3/search?part=snippet&order=date&q=%s&key=%s" % (urllib.quote(self.search_term, ""), self.api_key)
        if self.last_upload_time is not None:
            url += "&publishedAfter=" + self.last_upload_time
        req = urllib2.urlopen(url)
        response = json.load(req)
        if self.last_upload_time is not None:
            for video in response["items"][:3]: # limit to 3 videos
                message = BOLD + "[youtube]" + RESET + " \"" + video["snippet"]["title"] + "\" by " + video["snippet"]["channelTitle"]
                self._broadcast(message)

    def _broadcast(self, message):
        for name in self.on:
            if name in self.channels:
                self.channels[name].chat(message)
                
