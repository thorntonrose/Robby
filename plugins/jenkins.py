import logging
import re
import requests
from slackbot.bot import respond_to
from slackbot.bot import listen_to

BASE_URL = "http://10.116.0.10:8080"

JOB_checkES = { 
    "blue": "Success", "blue_anime": "Running", 
    "yellow": "Unstable", "yellow_anime": "Running", 
    "red": "Failed", "red_anime": "Running"
}

log = logging.getLogger(__name__)

def get_job_url(job):
   return "{}/job/{}".format(BASE_URL, job)

def reply_error(message, method, url, resp):
    message.reply("I got '{} {}' for '{} {}'.".format(resp.status_code, resp.reason, method, url))

@respond_to("jenkins run (.*)", re.IGNORECASE)
def jenkins_run(message, job):
    log.info("jenkins_run ...")
    params = "token=TOKEN"
    job_url = get_job_url(job)
    build_url = "{}/build?{}".format(job_url, params)
    log.info("jenkins_run: build_url: {}".format(build_url))
    resp = requests.post(build_url)
    log.info("jenkins_run: status_code: {}".format(resp.status_code))

    if (resp.status_code == 400):
        build_url = "{}/buildWithParameters?{}".format(job_url, params)
        log.info("jenkins_run: build_url: {}".format(build_url))
        resp = requests.post(build_url)
        log.info("jenkins_run: status_code: {}".format(resp.status_code))

    if (resp.status_code == 201):
        message.reply("I started {}. Check Slack or {} for results.".format(job, job_url))
    else:
        reply_error(message, "POST", build_url, resp)

@respond_to("jenkins check (.*)", re.IGNORECASE)
def jenkins_check(message, job):
    log.info("jenkins_check ...")
    job_url = get_job_url(job)
    status_url = "{}/api/json".format(job_url)
    log.info("jenkins_check: status_url: {}".format(status_url))
    resp = requests.get(status_url)

    if (resp.status_code == 200):
       job_data = resp.json()
       color = job_data["color"]
       last_build_url = job_data["lastBuild"]["url"]
       log.info("jenkins_check: color: {}, last_build_url: {}".format(color, last_build_url))
       message.reply("The status of {} is '{}'. Check {} for information on the last build.".format( \
           job, JOB_checkES[color], last_build_url))
    else:
        reply_error(message, "GET", status_url, resp)
