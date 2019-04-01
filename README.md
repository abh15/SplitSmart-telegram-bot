# SplitSmart-telegram-bot
A bot to keep track of split bills in telegram groups
### Requirements
1. Install python-telegram-bot 
```console
$ pip install python-telegram-bot --upgrade 
```
2. Get a bot token from @BotFather on telegram 

### Usage
Use the unique bot token while running this bot(line 130)


Add the bot to group before adding other members, else it will not keep track of usernames of members. This is due to API restrictions.


Use /start command to intialize ledger before adding any transaction
