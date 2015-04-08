# HP's Dragon
##A Slack Chat Bot

# Description

This is a bot for use with the Slack Chat webclient. It uses Slack's Web API format and is written in Python 3.

More info on Slack bots can be found [here.](https://api.slack.com/bot-users)

I call this "HP's Dragon", but it can easily be renamed within the file dragon.py (which can also be renamed).

The bot's commands can be found [here](https://github.com/jdenson/HP-s-Dragon/blob/master/COMMANDS.md)

# Installation
#### Python 3.x must be installed on any system attempting to run this bot.

## Normal (Linux)

This is a standalone program and as such it is easy to install.

Remember that you must be running (as) Python 3.4 or later.

1. Download or clone the repository to your target directory
2. Update the bot file ("dragon.py") with the necessary information provided to you by Slack
	1. To generate your CLIENT_ID and CLIENT_SECRET, you will need to register your bot [here](https://api.slack.com/applications/new)
	2. Assign the bot a username in the provided field.
	3. Make sure to include the necessary information such as Team and *your* username. The bot REQUIRES this info to function properly.
3. Update auth/token.txt with your API token (make sure the file only contains one line)
	1. You will need to generate your API token either with a new integration [here](https://my.slack.com/services/new/bot), or with your own Web API authentication [here](https://api.slack.com/web)
4. Once you have made sure that all necessary info has been added to the bot, activate a virtual environment.
5. As root, install the required dependencies with `pip3 install -r requirements.txt --allow-all-external`
6. Run the bot!

If the bot is working properly, after starting it will begin to display scrolling data output, beginning with a request/response header.

## Normal (Windows)
#### Remember that any system the bot is running on must remain on for the bot to function.

1. Follow steps 1-3 above.
2. Run either the command prompt (cmd.exe) or Powershell as an Administrator
3. `cd` to the repository folder.
4. Run the command `pip install -r requirements.txt --allow-all-external`
5. Run the bot, either by running it directly or from within the Python Shell.

If the bot is working properly, after starting it will begin to display scrolling data output, beginning with a request/response header.

## Heroku

This repository contains everything necessary for the bot to be run on Heroku.

Follow the normal Python deployment procedure to deploy and run the bot. Please note that if you rename the main bot file ("dragon.py") you must also update the Procfile accordingly.

I recommend using the Papertrail addon to track the output of the bot.