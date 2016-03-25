import logging
import logging.config
import sys

if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)
    log = logging.getLogger(__name__)

    from slackbot.bot import Bot
    Bot().run()