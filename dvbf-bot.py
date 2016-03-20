import socket
import re
import random
import time
# TODO: Imp module loading commands

channels = ["#fluffet"]

class IRCEvent(object):
    def __init__(self, line):
        m = re.search('^(?:[:](\S+) )?(\S+)(?: (?!:)(.+?))?(?: [:](.+))?$', line)
        self.raw_line = line
        self.host = ""
        self.channel = ""
        self.nick = ""
        self.message = ""
        self.event_type = m.group(2)

        if self.event_type == "PRIVMSG" or self.event_type == "JOIN":
            self.channel = m.group(3)
            self.nick = m.group(1).split("!")[1][1:]
            self.host = m.group(1).split("@")[1]
        
        if self.event_type == "PRIVMSG":
            self.message = m.group(4)

    def parse_privmsg(self):
        if self.message == "who's a good bot?":
            self.reply("me!")

    def parse_join(self):
        return

    def reply(self,message):
            client.send("PRIVMSG {0} :".format(self.channel) + message)

class IRCClient(object):
    def __init__(self, username, nickname=None, realname=None):
        self.username = username
        self.nickname = nickname or username
        self.real_name = realname or username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._can_join_channels_yet = False
    def connect(self, host):
        host, port = host.split(":")
        port = int(port)
        self.socket.connect((host,port))
        self.send("NICK {}".format(self.nickname))
        self.send("USER {} 0 * :{}".format(self.username, self.real_name))

    def send(self, data):
        self.socket.send( (data + "\r\n").encode() )
    
    def read_buffer_lines(self):
        buffer = ""
        while True:
            if "\r\n" not in buffer:
                buffer += self.socket.recv(512).decode("utf-8")
            line, buffer = buffer.split("\r\n", maxsplit=1)
            yield line
    def join_channel(self, channel_name):
        client.send("JOIN " + channel_name)

client = IRCClient("dvbf-bot","dvbf-bot","dvbf-bot")
client.connect("chat.freenode.net:6667")

def main():
    for line in client.read_buffer_lines():
        event = IRCEvent(line)
        
        if event.event_type == "PRIVMSG":
           event.parse_privmsg()
        elif event.event_type == "JOIN":
            event.parse_join()
    
        # Reply to PING to not get disconnected
        if line[0] == "PING":
            client.send("PONG" +line[1])
        # This string comp is unnecessary to do all the time
        elif not client._can_join_channels_yet:
            if line == ":{0} MODE {0} :+i".format(client.username):
                client._can_join_channels_yet = True
                for channel in channels:
                    client.join_channel(channel)
                    time.sleep(1)
    
if __name__ == '__main__':
    main()
