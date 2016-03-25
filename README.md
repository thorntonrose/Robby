# Robby the Chatbot

Robby is a chatbot for Slack.

## Setup

`pip install -r dependencies.txt`

## Usage

### Run

`./robby run <mode>`

Mode:

* dev = Connect to Slack as @robby-dev
* prod = Connect to Slack as @robby

### Start Daemon

`./robby start <mode>`

### Stop Daemon

`./robby stop <mode>`

### Chat

Login to mstv.slack.com and send direct messages to @robby. For a list of commands, say anything.

## Logging

Robby logs to robby.log in the current directory. Logging is configured via logging.ini.

## See Also

* [Robby's Configuration on Slack](https://mstv.slack.com/services/B0UGM757B)
* [Slackbot](https://github.com/lins05/slackbot)
* [Slack Bot Users](https://api.slack.com/bot-users)
* [Robby the Robot](https://en.wikipedia.org/wiki/Robby_the_Robot)

## Ideas for Commands

tests run <name> [branch=<branch>] [mdms=<mdms-ip>] [dns=<dns-ip>]

tests check [<name>] [branch=<branch>]

v1 show <id>

v1 show my work

v1 show burndown <team>