import logging
import logging.config
import slackbot_settings
import sys

if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)
    log = logging.getLogger(__name__)
    
    if len(sys.argv) > 0 and sys.argv[0] == "prod":
       slackbot_settings.API_TOKEN = slackbot_settings.API_TOKEN_PROD

    from slackbot.bot import Bot
    Bot().run()