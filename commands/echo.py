def execute(client, event, command_loader, log=None):
    if event.event_type == "PRIVMSG":
        if event.message.startswith("dvbf-bot.echo "):
            echo = event.message.split(" ",1)[1] 
            event.reply(echo)
            return True
    
    return False

def usage():
    return ".echo"

def help():
    return ".echo : echo everything after echo"
