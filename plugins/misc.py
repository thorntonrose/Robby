import json
import logging
import plugins.jenkins
import re
import requests
import slackbot_settings
from slackbot.bot import respond_to
from slackbot.bot import listen_to

log = logging.getLogger(__name__)

COMMANDS = [
    "`jenkins check <job>` -- Get status and URL of a Jenkins job.",
    "`jenkins run <job> [<parameter>=<value> ...]` -- Run a Jenkins job.",
    "`jenkins stop <job>` -- Stop a Jenkins job.",
    "`update self` -- Download code updates and restart.",
    "`version` -- Show version."
]

# message handlers ############################################################

@respond_to("help")
def help(message):
    log.debug("help ...")
    message.reply("Commands:\n{}".format("\n".join(COMMANDS)))

@respond_to("update self")
def update(message):
    log.debug("update ...")
    jenkins.run_job(message, "robby-update", "MODE=" + slackbot_settings.mode)

@respond_to("version")
def version(message):
    log.debug("version ...")
    with open("version.txt", "r") as file:
        message.reply("version {} ({})".format(file.read().strip(), slackbot_settings.mode))