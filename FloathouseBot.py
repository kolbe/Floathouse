#!/usr/bin/env python3

# https://python-telegram-bot.readthedocs.io/en/stable/

import logging
import os, sys
import socket
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

admin = [
        550700252 # Kolbe
        ]

l = logging
l.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

telegram_token = os.environ['TELEGRAM_TOKEN']

updater = Updater(token=telegram_token, use_context=True)
l.info("Successfully obtained Updater")
dispatcher = updater.dispatcher

def sendCmd(cmd):

    HOST, PORT = "127.0.0.1", 8765

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(cmd + "\n", "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")

    l.info("Sent:     {}".format(cmd))
    l.info("Received: {}".format(received))

def start(update, context):
    l.info("cmd /start: Starting!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
dispatcher.add_handler(CommandHandler('start', start))

def restart(update, context):
    l.info("cmd /restart: Restarting!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Restarting!")
    context.dispatcher.stop()
    os._exit(0)
dispatcher.add_handler(CommandHandler('restart', restart))

def exit(update, context):
    l.info("cmd /exit: Exiting!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Exiting!")
    #sys.exit()
    os._exit(0)
dispatcher.add_handler(CommandHandler('exit', exit))

def lights(update, context):
    l.info("cmd /lights [{}]".format(" ".join(context.args)))
    try:
        cmd = context.args[0]
        context.bot.send_message(chat_id=update.effective_chat.id, text="Executing command lights {}!".format(cmd))
        sendCmd(cmd)
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="ERROR: must provide an argument to the /lights command!")
dispatcher.add_handler(CommandHandler('lights', lights))

def echo(update, context):
    user = update.effective_user
    l.info('<{} ({})> {}'.format(user.full_name, user.id, update.message.text))
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
dispatcher.add_handler(MessageHandler(Filters.text, echo))

l.info("Callbacks registered, starting poll loop")
updater.start_polling()
