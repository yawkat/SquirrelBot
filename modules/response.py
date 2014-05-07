from module import Module

import re
import random

class Response(Module):
    def __init__(self, command_regex, responses):
        super(Response, self).__init__("response")
        self.command = re.compile(command_regex)

        if type(responses) is str:
            responses = [line.strip() for line in open(responses)] 

        self.responses = responses

    def on_chat(self, message):
        result = self.command.match(message.message)
        if result:
            response = random.choice(self.responses)
            response = response.format(*(result.groups()))
            message.channel.me(response)
