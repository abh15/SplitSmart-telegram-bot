#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A telegram Bot to keep track of split bills in a group
    
    Copyright (C) 2019 Abhishek Dandekar

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

membernames=[]  #array to keep track of member usernames
ledger = {}     #Main ledger for record

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def initilize_ledger():         #Initilizes ledger dictionary from current members 
        for currIndex,currUser in enumerate(membernames):   #currIndex gives array index while currUser provides actual value of that index
                for incvar in range(1,len(membernames)-currIndex):
                        ledger[currUser+">"+membernames[currIndex+incvar]] = 0 

def update_ledger_oto(sender,receiver,amount):      #Update ledger for one to one tx
        searchstr=sender+">"+receiver
        if ledger.get(searchstr)!=None:
                newval=ledger[searchstr]+amount
                ledger[searchstr]=newval
        else:
                searchstr=receiver+">"+sender
                newval=ledger[searchstr]-amount
                ledger[searchstr]=newval
      
def update_ledger_mto(senderArr,receiver,amount):       #Update ledger for many to one tx
        for sender in senderArr:
                searchstr=sender+">"+receiver
                if ledger.get(searchstr)!=None:
                        newval=ledger[searchstr]+amount
                        ledger[searchstr]=newval
                else:
                        searchstr=receiver+">"+sender
                        newval=ledger[searchstr]-amount
                        ledger[searchstr]=newval


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hej!')
    initilize_ledger()
    update.message.reply_text('I am ready to record transactions')

def lm(bot, update):
        update.message.reply_text(membernames)

def oto(bot, update):   #Parse incoming string and send it to ledger updater func
        s=update.message.text
        update_ledger_oto(s.split()[1],s.split()[2],float(s.split()[3]))

def mto(bot, update):   #Parse incoming string and send it to ledger updater func
        s=update.message.text
        update_ledger_mto(s.split()[1].split(','),s.split()[2],float(s.split()[3]))     

def settle(bot, update):        #Pretty print the current ledger state
        ledger_state=""
        for entry in ledger:    #Change the message depending on amount is positive,negative or zero
                if ledger[entry]<0:
                    ledger_state= ledger_state + entry.split('>')[1]+" OWES "+entry.split('>')[0]+' SEK '+str(-ledger[entry])+"\n"
                elif ledger[entry]==0:
                        ledger_state= ledger_state + entry.split('>')[0]+" OWES "+entry.split('>')[1]+" NOTHING\n"
                else:
                        ledger_state= ledger_state + entry.split('>')[0]+" OWES "+entry.split('>')[1]+' SEK '+str(ledger[entry])+"\n"
        
        update.message.reply_text(ledger_state)

def help(bot, update):
    """Send a message when the command /help is issued."""
    msg=str()
    msg +=    """ 
        After all members are added in group make sure to use start command before starting any transactions 
        /start - Initialize the Ledger\n
        /lm - List usernames of group members\n
        /settle - See latest debt\n
        /oto  - One to one transaction\n /oto <SenderUsername> <ReceiverUsername> <Amount in SEK>\n
        /mto - Many to one transaction\n /mto <SenderUsername1,SenderUsername2,SenderUsername3> <ReceiverUsername> <Amount in SEK>\n
     
     """
     

    bot.send_message(chat_id=update.message.chat_id, text=msg,parse_mode="Markdown")
    #update.message.reply_text(text=msg)   



def track_member(bot, update):  #not a command, used internally to identify new members
    ''' here you receive a list of new members (User Objects) in a single service message'''
    new_members = update.message.new_chat_members
    # do your stuff here:
    for member in new_members:
        #print(member.username)
        #update.message.reply_text(member.username)
        membernames.append(member.username)     

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    #updater = Updater("<Your bot token here>")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("lm", lm))
    dp.add_handler(CommandHandler("mto", mto))
    dp.add_handler(CommandHandler("oto", oto))
    dp.add_handler(CommandHandler("settle", settle))

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, track_member))        #handle new member added updates

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
