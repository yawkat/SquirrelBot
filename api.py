import irc.client
import threading
import sys
import Queue
import traceback

class Connection(object):
    def __init__(self, nick, host, port):
        self.nick = nick
        self.host = host
        self.port = port

        self._handlers = {}

        self._execution_queue = Queue.Queue()

    def connect(self, callback):
        self._login_callback = callback
        self._manifold = irc.client.Manifold()
        self._manifold.add_global_handler("all_events", self._event)

        self._add_handler("welcome", self._welcome)

        self._connection = self._manifold.server().connect(self.host, self.port, self.nick, None, ircname=self.nick)

        for i in range(4):
            threading.Thread(target=self._work).start()

        self._execute(self._listen)

        return self

    def disconnect(self):
        self._connection.disconnect()

    def join(self, name, callback, key = ""):
        assert name is not ''

        if name[0] is not '#':
            name = '#' + name
        channel = Channel(self, name, callback, key)
        self._execute(channel._join)
        return channel

    def _work(self):
        while 1:
            task = self._execution_queue.get(block=True)
            try:
                task()
            except:
                traceback.print_exc()

    def _execute(self, task):
        self._execution_queue.put(task)

    def _listen(self):
        print "Listening for events..."
        self._manifold.process_forever()

    def _welcome(self, evt):
        print "Welcome " + self.nick + " to " + self.host + ":" + str(self.port)
        self._login_callback(self)

    def _add_handler(self, evt_type, handler):
        if not evt_type in self._handlers:
            self._handlers[evt_type] = []
        self._handlers[evt_type].append(handler)

    def _event(self, connection, evt):
        # print "Event " + evt.type
        if evt.type in self._handlers:
            for handler in self._handlers[evt.type]:
                self._execute(lambda evt=evt, handler=handler: handler(evt))

class Channel(object):
    def __init__(self, connection, name, join_callback, key):
        self.connection = connection
        self.name = name
        self._join_callback = join_callback
        self.key = key

    def _join(self):
        print "Joining " + self.name
        self.connection._connection.join(self.name, self.key)
        self._join_callback(self)

    def leave(self):
        self.connection._connection.part(self.name)

    def send(self, message):
        message._run(self)

    def chat(self, message):
        self.send(Chat(message))

    def me(self, message):
        self.send(Me(message))

    def add_chat_listener(self, listener):
        self.connection._add_handler("pubmsg", lambda evt, listener=listener: self._call_chat(listener, evt))

    def _call_chat(self, listener, evt):
        if evt.target == self.name:
            listener(ReceivedChat(self, evt.source[:evt.source.find("!")], evt.arguments[0]))

class SendableMessage(object):
    def _run(channel):
        pass

class Chat(SendableMessage):
    def __init__(self, message):
        self.message = message

    def _run(self, channel):
        print "Sending " + self.message
        channel.connection._connection.privmsg(channel.name, self.message)

class Me(Chat):
    def __init__(self, message):
        super(Me, self).__init__("\x01ACTION " + message + "\x01")

class ReceivedMessage(object):
    pass

class ReceivedChat(ReceivedMessage):
    def __init__(self, channel, sender, message):
        self.channel = channel
        self.sender = sender
        self.message = message