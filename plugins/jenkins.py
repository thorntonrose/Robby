import logging
import re
import requests
from slackbot.bot import respond_to
from slackbot.bot import listen_to

BASE_URL = "http://10.116.0.10:8080"

JOB_STATUSES = { 
    "red": "Failed",
    "yellow": "Unstable", 
    "blue": "Success", 
    "grey": "Pending",
    "disabled": "Disabled",
    "aborted": "Aborted",
    "notbuilt": "Not Built"
}

log = logging.getLogger(__name__)

def get_job_url(job):
   return "{}/job/{}".format(BASE_URL, job)

def get_job_status(job_data, color):
   if color.endswith("_anime"): return "In Progress"
   return JOB_STATUSES[color]

def reply_error(message, method, url, resp):
    log.debug("reply_error ...")
    message.reply("I got '{} {}' for '{} {}'.".format(resp.status_code, resp.reason, method, url))

@respond_to("jenkins run (.*)", re.IGNORECASE)
def jenkins_run(message, job):
    log.debug("jenkins_run ...")
    params = "token=TOKEN"
    job_url = get_job_url(job)
    build_url = "{}/build?{}".format(job_url, params)
    log.debug("jenkins_run: build_url: {}".format(build_url))
    resp = requests.post(build_url)
    log.debug("jenkins_run: status_code: {}".format(resp.status_code))

    if resp.status_code == 400:
        build_url = "{}/buildWithParameters?{}".format(job_url, params)
        log.debug("jenkins_run: build_url: {}".format(build_url))
        resp = requests.post(build_url)
        log.debug("jenkins_run: status_code: {}".format(resp.status_code))

    if resp.status_code == 201:
        message.reply("{} started: {}".format(job, job_url))
    else:
        reply_error(message, "POST", build_url, resp)

@respond_to("jenkins check (.*)", re.IGNORECASE)
def jenkins_check(message, job):
    log.debug("jenkins_check ...")
    job_url = get_job_url(job)
    status_url = "{}/api/json".format(job_url)
    log.debug("jenkins_check: status_url: {}".format(status_url))
    resp = requests.get(status_url)

    if (resp.status_code == 200):
       job_data = resp.json()
       color = str(job_data["color"])
       status = get_job_status(job_data, color)
       last_build_url = job_data["lastBuild"]["url"]
       log.debug("jenkins_check: color: {}, status: {}, last_build_url: {}".format(color, status, last_build_url))
       message.reply("{} status: {}, last build: {}".format(job, status, last_build_url))
    else:
        reply_error(message, "GET", status_url, resp)