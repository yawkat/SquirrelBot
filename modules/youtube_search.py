from module import StatusModule
from irc_format import *

import urllib
import urllib2
import json
import time
import traceback
import threading

class YoutubeSearch(StatusModule):
    def __init__(self, id, api_key, channels, search_term):
        super(YoutubeSearch, self).__init__(id, on=channels, rate=30)
        self.api_key = api_key
        self.channels = channels
        self.search_term = search_term

        self.last_upload_time = None

    def _poll(self):
        url = "https://www.googleapis.com/youtube/v3/search?part=snippet&order=date&q=%s&key=%s" % (urllib.quote(self.search_term, ""), self.api_key)
        if self.last_upload_time is not None:
            url += "&publishedAfter=" + urllib.quote(self.last_upload_time, "")
        req = urllib2.urlopen(url)
        response = json.load(req)
        if self.last_upload_time is not None:
            for video in response["items"][:3]: # limit to 3 videos
                if video["snippet"]["publishedAt"] == self.last_upload_time:
                    break
                message = BOLD + "[youtube]" + RESET + " \"" + video["snippet"]["title"] + "\" by " + video["snippet"]["channelTitle"]
                self._broadcast(message)
        if len(response["items"]) is not 0:
            self.last_upload_time = response["items"][0]["snippet"]["publishedAt"]
                
