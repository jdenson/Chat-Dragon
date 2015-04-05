# HP's Dragon
A Slack Chat Bot


This is a bot for use with the Slack Chat webclient. It uses Slack's Web API format and is written in Python 3.

More info on Slack bots can be found here: https://api.slack.com/bot-users

To generate your CLIENT_ID and CLIENT_SECRET, you will need to register your bot here: https://api.slack.com/applications/new

You will also need to generate your API token either with a new integration here: https://my.slack.com/services/new/bot or with your own Web API authentication here: https://api.slack.com/web


COMMANDS TO THE DRAGON ARE AS FOLLOWS:

(Only fully implemented commands are shown for now.)

 !flame username -- will taunt user
 
 !praise username -- will praise user
 
 !pic search_string -- will display a random picture after searching google for search_string
 
 !iplay game1 game2 game3 -- will record that you are playing game1 game2 game3
 
 !whoplays game -- will list all people who have reported that they play game
 
 !playing name -- will list every game name is playing
 
 !quote -- put up a random quote
 
 !suggest game -- will choose a game from the list of all games people are playing
 
 +amount name -- assign amount DKP to name
 
 -amount name -- remove amount DKP from name
 
 !joke -- offer a random joke
 
 !roll -- return a random number between 0 and 10000
 
 !stock ticker -- get the current quote for ticker
 
 !coin coinname -- get the current price of crypt currency <coin>
 
 !record username -- record the last thing username said.
 
 !test -- make sure the bot is responding