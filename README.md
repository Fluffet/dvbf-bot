#dvbf-bot
Shitty IRC bot. Created one because I have always wanted to create one :)
###features
  - Modular command/plugin loading, and it's dynamic too -- no need to restart the bot
  - Some basic plugins (more will be added as I figure out what to add)

###Instructions
The two base classes, IRCClient and IRCEvent should be pretty self documenting. Basically, the IRCEvent class should contain everything you need to write some sort of plugin, and it's .reply(message) method should be called if you want to reply something to the same channel where the event is from.

To create a plugin, just follow the structure of the already existing ones. Since they are seperate files, you can do your own imports and "advanced" plugins that do whatever you want.

###TODO: 
  - Make it learn to imitate others by parsing logs with Markov chaining
  - Some sort of exception handling for crashing plugins, and write error message if these are executed

