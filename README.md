# Robby the Chatbot

Robby is a chatbot for Slack.

## Setup

`pip install -r dependencies.txt`

## Usage

### Run

`python robby.py <mode>`

Mode:

* dev = Connect to Slack as @robby-dev
* prod = Connect to Slack as @robby

### Start Daemon

`./robby start <mode>`

### Stop Daemon

`./robby stop <mode>`

### Usage

Send direct messages to @robby. For a list of commands, send anything.

## Logging

Robby logs to robby.log in the current directory. Logging is configured via logging.ini.

## See Also

* [Slackbot](https://github.com/lins05/slackbot)
* [Slack Bot Users](https://api.slack.com/bot-users)
* [Robby the Robot](https://en.wikipedia.org/wiki/Robby_the_Robot)

## Ideas for Commands

tests run <name> [branch=<branch>] [host=<ip>] [dns=<ip>]

tests check [<name>] [branch=<branch>]

v1 show <id>

v1 show my work

v1 show burndown <team>