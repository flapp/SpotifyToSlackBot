# SpotifyToSlackBot
Simple spotify to slack integration that uses AppleScript for bindings to spotify

** Configuration: **
rename config.ini.example to config.ini and add your bot api key, and bot name
(You can make this at: https://api.slack.com/bot-users)

** Usage: **
Source the current init-environment.sh (for example by running: '. ./init-environment.sh' in bash
now run the bot by executing BotMain.py

now invite the bot to your channel by running /invite <botname> in the slack channel you want. 
The bot will output your current song if it gets highlighted with its username and /spotify
(For example: @mysuperbot /spotify)
