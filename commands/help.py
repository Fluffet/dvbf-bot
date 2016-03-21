def execute(client, event, command_loader, log=None):
    if event.event_type == "PRIVMSG":
        if event.message.startswith("dvbf-bot.help "):
            command = event.message.split(" ",1)[1] + ".py"
            try:
                print(command)
                if command_loader.loaded_commands[command] != None:
                    event.reply(command_loader.loaded_commands[command].help())
            except KeyError:
                event.reply("Could not find a command by that name. Try dvbf-bot.commands")
            return True
    
    return False

def usage():
    return ".help"

def help():
    return ".help : .help x    where x = command displays some help string"
