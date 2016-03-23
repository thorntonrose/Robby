import logging
import logging.config
import sys
from slackbot.bot import Bot

if __name__ == "__main__":
    # logging.basicConfig(**{
    #     'format': '[%(asctime)s] %(message)s',
    #     'datefmt': '%m/%d/%Y %H:%M:%S',
    #     'level': logging.INFO,
    #     'stream': sys.stdout,
    # })

    logging.config.fileConfig("logging.ini")
    logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)
    log = logging.getLogger(__name__)
    log.info("run ...")
    Bot().run()