def execute(client, event, command_loader, log=None):
    if event.event_type == "PRIVMSG":
        if event.message == "dvbf-bot.source_code":
            event.reply("Source code available at: https://github.com/Fluffet/dvbf-bot/")
            return True

    return False

def usage():
    return ".source_code"

def help():
    return ".source_code | types https://github.com/Fluffet/dvbf-bot/"
