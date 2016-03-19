import socket

class IRCClient(object):
    def __init__(self, username, nickname=None, realname=None):
        self.username = username
        self.nickname = nickname or username
        self.real_name = realname or username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host):
        host, port = host.split(":")
        port = int(port)
        self.socket.connect((host,port))
        self.send("NICK {}".format(self.nickname))
        self.send("USER {} 0 * :{}".format(self.username, self.real_name))

    def send(self, data):
        self.socket.send( (data + "\r\n").encode() )
    
    def read_lines(self):
        buffer = ""
        while True:
            if "\r\n" not in buffer:
                buffer += self.socket.recv(512).decode("utf-8")
            line, buffer = buffer.split("\r\n", maxsplit=1)
            yield line

client = IRCClient("dvbf-bot","dvbf-bot","dvbf-bot")
client.connect("chat.freenode.net:6667")

for line in client.read_lines():
    print(line)
