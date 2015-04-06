# HP's Dragon
##A Slack Chat Bot

# Description

This is a bot for use with the Slack Chat webclient. It uses Slack's Web API format and is written in Python 3.

More info on Slack bots can be found [here.](https://api.slack.com/bot-users)

I call this "HP's Dragon", but it can easily be renamed within the file dragon.py (which can also be renamed).

The bot's commands can be found [here](https://github.com/jdenson/HP-s-Dragon/blob/master/COMMANDS.md)

# Installation

This is a standalone program and as such it is easy to install.

Remember that you must be running (as) Python 3.4 or later.

1. Download or clone the repository to your target directory
2. Update the bot file ("dragon.py") with the necessary information provided to you by Slack
	1. To generate your CLIENT_ID and CLIENT_SECRET, you will need to register your bot [here](https://api.slack.com/applications/new)
	1. Assign the bot a username in the provided field.
        2. Make sure to include the necessary information such as Team and *your* username. The bot REQUIRES this info to function properly.
3. Update token.txt with your API token (make sure the file only contains one line)
	1. You will need to generate your API token either with a new integration [here](https://my.slack.com/services/new/bot), or with your own Web API authentication [here](https://api.slack.com/web)
4. (Optional) Once you have made sure that all necessary info has been added to the bot, activate a virtual environment.
5. Install the required dependencies with `pip(3) install -r requirements.txt --allow-all-external`
6. Run the bot!

If the bot is working properly, after starting it will begin to display scrolling data output, beginning with a request/response header.
