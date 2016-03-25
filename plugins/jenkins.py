import json
import logging
import re
import requests
from slackbot.bot import respond_to
from slackbot.bot import listen_to

log = logging.getLogger(__name__)

BASE_URL = "http://10.116.0.10:8080"

STATUS_COLOR_NAMES = { 
    "red": "failed",
    "yellow": "unstable", 
    "blue": "success", 
    "grey": "pending",
    "disabled": "disabled",
    "aborted": "aborted",
    "notbuilt": "not built"
}

STATUS_IN_PROGRESS = "in progress"
STATUS_IN_QUEUE = "in queue"

# utility functions ###########################################################

def get_job_url(job):
    return "{}/job/{}".format(BASE_URL, job)

def get_job_info_url(job):
    return "{}/api/json".format(get_job_url(job))

def get_status_for_color(color):
    return STATUS_IN_PROGRESS if color.endswith("_anime") else STATUS_COLOR_NAMES[color]

def get_status(job_info):
    return STATUS_IN_QUEUE if job_info['inQueue'] else get_status_for_color(job_info['color'])

def build_query_string(args):
    params = "&".join([ a for a in args.split(" ") if '=' in a.strip() ]) if args else ""
    return "?" + params if params else ""

def reply_error(message, method, url, resp):
    log.debug("reply_error ...")
    message.reply("error: '{} {}' from '{} {}'".format(resp.status_code, resp.reason, method, url))

def get_job_info(message, job):
    log.debug("get_job_info ...")
    info_url = get_job_info_url(job)
    log.debug("get_job_info: info_url: {}".format(info_url))
    resp = requests.get(info_url)
    log.debug("get_job_info: status_code: {}".format(resp.status_code))

    if resp.status_code == 200:
        return resp

    if resp.status_code == 404:
        message.reply("{}: not found".format(job))
        return None

    reply_error(message, "GET", info_url, resp)
    return None

def post(message, url, success_codes):
    log.debug("post: url: {} ...".format(url))
    resp = requests.post(url)
    log.debug("post: status_code: {}".format(resp.status_code))

    if resp.status_code in success_codes:
        log.debug("post: status_code in {}".format(success_codes))
        return resp

    message.reply_error(message, "POST", url, resp)
    return None

# message handlers ############################################################

# jenkins check <job>
@respond_to("jenkins\s+check\s+([a-zA-Z0-9-_]+)", re.IGNORECASE)
def check_job(message, job):
    log.debug("check_job ...")
    # log.debug("check_job: message: {}".format(json.dumps(message._body)))
    resp = get_job_info(message, job)

    if resp:
        job_info = resp.json()
        status = get_status(job_info)

        if status != STATUS_IN_QUEUE and job_info['lastBuild']:
            url = job_info['lastBuild']['url']
        else:
            url = get_job_url(job)

        log.debug("check_job: status: {}, url: {}".format(status, url))
        message.reply("{}: {}, {}".format(job, status, url))

# jenkins run <job> [<args>]
@respond_to("jenkins\s+run\s+([a-zA-Z0-9-_]+)(.*)", re.IGNORECASE)
def run_job(message, job, args):
    log.debug("run_job: job: {}, args: {} ...".format(job, args))
    resp = get_job_info(message, job)

    if resp:
        job_info = resp.json()
        job_url = get_job_url(job)

        if "parameterDefinitions" in job_info['actions'][0]:
            query_string = build_query_string(args)
            log.debug("run_job: query_string: {}".format(query_string))
            build_url = "{}/buildWithParameters{}".format(job_url, query_string)
        else:
            query_string = ""
            build_url = "{}/build".format(job_url)
        
        resp = post(message, build_url, [ 201 ])

        if resp:
            params = query_string[1:] if query_string else "no parameters"
            message.reply("{}: started with {}, {}".format(job, params, job_url))

# jenkins stop <job>
@respond_to("jenkins\s+stop\s+([a-zA-Z0-9-_]+)", re.IGNORECASE)
def stop_job(message, job):
    log.debug("stop_job: job: {} ...".format(job))
    resp = get_job_info(message, job)

    if resp:
        job_info = resp.json()
        status = get_status(job_info)
        log.debug("stop_job: status: {}".format(status))

        if status == STATUS_IN_QUEUE:
            queue_item_id = job_info['queueItem']['id']
            stop_url = "{}/queue/cancelItem?id={}".format(BASE_URL, queue_item_id)
            resp = post(message, stop_url, [ 302, 404 ])

            if resp and resp.status_code == 404:
                message.reply("{}: dequeued, {}".format(job, get_job_url(job)))
                return

        stop_url = "{}/stop".format(job_info['lastBuild']['url'])
        resp = post(message, stop_url, [ 200, 302 ])

        if resp:
            message.reply("{}: interrupted, {}\n(It will take a few seconds for the job to stop.)".format( \
                job, get_job_url(job)))

# jenkins run <name> tests
# jenkins run <name> tests <mdms-ip>
# jenkins run <name> tests <mdms-ip> <dns-ip>