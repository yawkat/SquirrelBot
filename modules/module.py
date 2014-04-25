class Module(object):
    def __init__(self, id):
        self.id = id
        self.channels = {}

    def on_chat(self, message):
        pass

    def init(self):
        pass