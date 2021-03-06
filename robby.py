import logging
import logging.config
import slackbot_settings
import sys

API_TOKENS = {
    "dev": "",
    "prod": ""
}

if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)
    log = logging.getLogger(__name__)

    if len(sys.argv) > 1:
        slackbot_settings.mode = sys.argv[1]
        slackbot_settings.API_TOKEN = API_TOKENS[slackbot_settings.mode]
        from slackbot.bot import Bot
        Bot().run()
    else:
       print("Usage: python robby.py {dev|prod}")