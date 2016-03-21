def execute(client, event, command_loader, log=None):
    if event.event_type == "PRIVMSG":
        if event.message == "dvbf-bot.commands":
            s = "Usage: dvbf-bot.command | My commands:"
            for command, module in command_loader.loaded_commands.items():
                s += " " + module.usage()
            
            event.reply(s)
            return True
    
    return False

def usage():
    return ".commands"

def help():
    return ".commands : Lists all commands"
