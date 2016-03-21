def execute(client, event, log=None):
    if event.event_type == "PRIVMSG":
        if event.message == "hi dvbf-bot":
            event.reply("Hello" + event.nick)
            return True
    
    return False
