import socket
import re
import time
import threading
import os
import imp

channels = ["#reddit-dailyprogrammer"]
nickname = "dvbf-bot"
irc_server = "chat.freenode.net:6667"

class DynamicCommandFileLoader(object):
    """This class loads commands once every (delay=60) without having to restart the bot"""
    
    def __init__(self):
        self.loaded_commands = {} 
        self.worker_thread = threading.Thread(target=self.reload_loop)
        self.worker_thread.start()

    def scan_commands(self):
        for command in os.listdir("commands/"):
            if command.endswith('.py'):
                self.import_command(command)
    
    def import_command(self,command):
        src = imp.load_source(command, "commands/" + command)
        self.loaded_commands[command] = src
        print("Imported: " + command)
    
    def reload_loop(self,delay=20):
        while True:
            self.scan_commands()
            
            time.sleep(delay)

class IRCEvent(object):
    """Base class to represent all IRC events from the server, by accessing event_type
    you can find out what it is and then access the proper members"""
    
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

    def reply(self,message):
            client.send("PRIVMSG {0} :".format(self.channel) + message)

class IRCClient(object):
    """Base class to interact with the IRC server"""

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
        """ This is an infinite buffer line generator, 
        it reads from the server and returns complete lines """
        buffer = ""
        while True:
            if "\r\n" not in buffer:
                buffer += self.socket.recv(512).decode("utf-8")
            line, buffer = buffer.split("\r\n", maxsplit=1)
            yield line
    def join_channel(self, channel_name):
        client.send("JOIN " + channel_name)

command_loader = DynamicCommandFileLoader()

client = IRCClient(nickname,nickname,nickname)
client.connect(irc_server)

def main():
    for line in client.read_buffer_lines():
        event = IRCEvent(line)
        
        for command,imported_module in command_loader.loaded_commands.items():
            executed = imported_module.execute(client, event, command_loader)
            if executed:
                break
                
    
        # Reply to PING to not get disconnected
        if line[0] == "PING":
            client.send("PONG" +line.split(" ")[1])
        # This string comp is unnecessary to do all the time
        elif not client._can_join_channels_yet:
            if line == ":{0} MODE {0} :+i".format(client.username):
                client._can_join_channels_yet = True
                for channel in channels:
                    client.join_channel(channel)
                    time.sleep(1)
    
if __name__ == '__main__':
    main()
