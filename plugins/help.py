import json
import logging
import re
import requests
from slackbot.bot import respond_to
from slackbot.bot import listen_to

COMMANDS = [
    "jenkins check <job>",
    "jenkins run <job> [<parameter>=<value> ...]",
    "jenkins stop <job>"
]

@respond_to("help")
def help(message):
    message.reply("Commands:\n{}".format("\n".join(COMMANDS)))