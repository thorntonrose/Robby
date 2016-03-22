import logging
import re
import requests
from slackbot.bot import respond_to
from slackbot.bot import listen_to

JENKINS_URL = "http://10.116.0.10:8080"
log = logging.getLogger(__name__)

@respond_to('jenkins run (.*)', re.IGNORECASE)
def jenkins_run(message, job):
    log.info("jenkins_run ...")
    params = "token=TOKEN"
    url = "{}/job/{}/build?{}".format(JENKINS_URL, job, params)
    log.info("jenkins_run: url: {}".format(url))
    resp = requests.post(url)
    log.info("jenkins_run: status_code: {}".format(resp.status_code))

    if (resp.status_code == 404):
        message.reply("Job {} not found at {}.".format(JENKINS_URL))
        return

    if (resp.status_code == 400):
        url = "{}/job/{}/buildWithParameters?{}".format(JENKINS_URL, job, params)
        log.info("jenkins_run: url: {}".format(url))
        resp = requests.post(url)
        log.info("jenkins_run: status_code: {}".format(resp.status_code))

    if (resp.status_code == 201):
        message.reply("Job {} queued. Check Slack or {}/job/{} for results.".format(job, JENKINS_URL, job))
    else:
        message.reply("Job {} not queued: {}, {}".format(resp.status_code, resp.text))