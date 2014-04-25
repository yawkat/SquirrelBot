from module import Module

class Test(Module):
    def __init__(self):
        super(Test, self).__init__("test")

    def on_chat(self, message):
        if message.message == ".ping":
            message.channel.chat("pong")