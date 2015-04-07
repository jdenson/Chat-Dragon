#!/usr/bin/env python3

import re
import json
import time
import random
import urllib
import urllib3
import websocket
import urllib.request
from threading import Thread
from datetime import datetime

CLIENT_ID = "<your_client_id>"
CLIENT_SECRET = "<your_client_secret>"
TEAM = "<your_slack_team_name>"
USER = "<your_slack_username>"
EXCHANGE_COUNT = 1
INFO = {}
INFO["name"] = "<your_bot's_username>" #may contain spaces/letters/numbers/some special characters, but I wouldn't overdo it
INFO["users"] = {}
INFO["channels"] = {}
RECENT_MESSAGES = {}
NOW = datetime.now()
USERNAME = urllib.request.quote(INFO["name"]) #formats the bot username to work properly with the WEB API url input

#opens and reads the file containing your API token
infile = open("token.txt")
TOKEN = infile.read()
infile.close()

def importInsults(filename="insults.txt"):
    infile = open(filename)
    insults = infile.readlines()
    infile.close()
    return insults

def importCompliments(filename="compliments.txt"):
    infile = open(filename)
    compliments = infile.readlines()
    infile.close()
    return compliments

def importQuotes(filename="quotes.txt"):
    infile = open(filename)
    quotes = infile.readlines()
    infile.close()
    return quotes

def importJokes(filename="jokes.txt"):
    infile = open(filename)
    jokes = infile.readlines()
    infile.close()
    return jokes
	
def importRPS(filename="rps.txt"):
    infile = open(filename)
    rps = infile.readlines()
    infile.close()
    return rps

COMPLIMENTS = importCompliments()
INSULTS = importInsults()
QUOTES = importQuotes()
JOKES = importJokes()

def getChannelID(channelName):
    try: return INFO["channels"][channelName]["id"]
    except KeyError: return ""

def getUserID(username):
    try: return INFO["users"][username]["id"]
    except KeyError: return ""

def getChannelName(channelID):
    try: return INFO["channels"][channelID]["name"]
    except KeyError: return ""

def getUserName(userID):
    try: return INFO["users"][userID]["name"]
    except KeyError: return ""

def updateSelfInfo(infoDict):
    INFO["selfID"] = infoDict["id"]

def updateUserList(infoDict):
    for eachDict in infoDict:
        userInfo = {}
        userInfo["ID"] = eachDict["id"]
        try: userInfo["name"] = eachDict["name"]
        except KeyError: userInfo["name"] = ""
        try: userInfo["bot"] = eachDict["is_bot"]
        except KeyError: userInfo["bot"] = False
        INFO["users"][userInfo["ID"]] = userInfo
        INFO["users"][userInfo["name"]] = userInfo

def updateChannelList(infoDict):
    for eachDict in infoDict:
        channelInfo = {}
        channelInfo["ID"] = eachDict["id"]
        channelInfo["name"] = eachDict["name"]
        INFO["channels"][channelInfo["ID"]] = channelInfo
        INFO["channels"][channelInfo["name"]] = channelInfo

def authenticateDragon():
    url = "https://slack.com/api/rtm.start?token=" + TOKEN
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    info = json.loads(str_response)
    if info["ok"] == True:
        updateSelfInfo(info["self"])
        updateUserList(info["users"])
        updateChannelList(info["channels"])
        return info["url"]
    else:
        print("not OK:", info)
        raise Exception("Authentication Failure")

#This should send the appropriate string back to slack using their WebAPI format. We also set the global variables needed to call the delete function.
#We also tell the bot to print the last string sent, the channel, and timestamp
def chat(ws, text, channel="spam"):
    global TSLAST
    global CHANLAST
    channelID = channel 
    print(getChannelName(channelID))
    print(text)
    text = urllib.request.quote(text)
    infile = urllib.request.urlopen("https://slack.com/api/chat.postMessage?token=" + TOKEN + "&channel=" + channelID + "&text=" + text + "&username=" + USERNAME + "&pretty=1")
    str_response = infile.readall().decode('utf-8')
    info = json.loads(str_response)
    TSLAST = info["ts"]
    CHANLAST = info["channel"]
    infile.close()
    print(TSLAST)
    print(CHANLAST)

#this defines how the bot deals with an incoming request
def onMessage(ws, message):
    info = json.loads(message)
    if "type" not in info: return
    if info["type"] == "message":
        try: userID = info["user"]
        except: return
        text = info["text"]
        RECENT_MESSAGES[getUserName(userID)] = text
        channelID = info["channel"]
        lower = text.lower()
#        if lower.find("!time") > -1: getTime(ws, userID, channelID) #display time
        if lower.find("!flame") > -1: flame(ws, userID, text, channelID) #insult user
        if lower.find("!praise") > -1: praise(ws, userID, text, channelID) #praise user
        if lower.find("!pic") > -1: getPic(ws, text, channelID) #search for and display picture matching input string
#        if lower.find("!define") > -1: defineWord(ws, text, channelID) #dictionary.com lookup
        if lower.find("!iplay") > -1: updatePlaying(ws, userID, text, channelID) #update which games the user is playing
        if lower.find("!whoplays") > -1: whoPlays(ws, text, channelID) #return results for user playing specified game
        if lower.find("!playing") > -1: getPlaying(ws, userID, text, channelID) #return results for what specified user is playing
        if lower.find("!quote") > -1: getQuote(ws, channelID) #display random quote
        if lower.find("!suggest game") > -1: suggestGame(ws, channelID) #suggest a game to play from playing.txt
        if lower[0] == '-' or lower[0] == '+': adjustDKP(ws, userID, text, channelID) #adjust user's "cool points"
        if lower.find("!joke") > -1: getJoke(ws, channelID) #display a random joke
        if lower.find("!roll") > -1: roll(ws, userID, text, channelID) #roll a die
        if lower.find("!help") > -1: sendHelp(ws, userID, channelID) #display dragon commands
        if lower.find("!stock") > -1: stockCheck(ws, userID, text, channelID) #yahoo finance lookup
        if lower.find("!coin") > -1: coinPrice(ws, userID, text, channelID) #check digital currency price
        if lower.find("!record") > -1: recordQuote(ws, userID, text, channelID) #record the last thing specified user said
#        if lower.find("!urbandefine") >-1: urbanDefine(ws, text, channelID) #urban dictionary lookup
        if lower.find("!test") >-1: dragonTest(ws, text, channelID) #make sure the dragon is alive
#        if lower.find("!deletethat") >-1: deleteThat(ws, TSLAST, CHANLAST) #tell the bot to delete its last message

#bot messages cannot currently be deleted with chat.delete (or at all for that matter). No ETA on this function. Leaving it in for posterity.
'''def deleteThat(ws, TSLAST, CHANLAST):
    infile = urllib.request.urlopen("https://slack.com/api/chat.delete?token=" + TOKEN + "&ts=" + TSLAST + "&channel=" + CHANLAST + "&pretty=1")
    infile.close()'''

'''def getTime(ws, text, channelID):
    chat(ws, "Get a watch.", channelID) '''

def flame(ws, userID, text, channelID):
    try: username = text.split(' ')[1]
    except IndexError: return
    isUser = getUserName(username)
    if isUser == "":
        chat(ws, "I don't know '%s' but I'm sure they're trouble." % username, channelID)
    else:
        chat(ws, "%s, %s" % (username, INSULTS[random.randrange(len(INSULTS))]), channelID)

def praise(ws, userID, text, channelID):
    try: username = text.split(' ')[1]
    except IndexError: return
    isUser = getUserName(username)
    if isUser == "":
        chat(ws, "I don't know '%s' but I'm sure they're nice." % username, channelID)
    else:
        chat(ws, "%s, %s" % (username, COMPLIMENTS[random.randrange(len(COMPLIMENTS))]), channelID)

def getPic(ws, text, channelID):
    baseURL = "http://www.bing.com/images/search?q="
    query = text.split(' ')
    if len(query) > 1:
        words = query[1:]
    else: words = ["funny"]
    url = ""
    for i in range(len(words)):
        url = url + words[i] + "+"
    url = url[:-1]
    fullURL = baseURL + url
    data = urllib.request.urlopen(fullURL).readall().decode('utf-8')
    urls = re.findall("imgurl:&quot;(.*?)[&#]", data)
    if len(urls) == 0:
        print(data)
        return
    imgURL = urls[random.randrange(len(urls))]
    chat(ws, imgURL, channelID)

#not yet fully implemented.
'''def defineWord(ws, text, channelID):   
    chat(ws, "would define word but on break", channelID) '''

def updatePlaying(ws, userID, text, channelID):
    username = getUserName(userID)
    try: PLAYING[username] = text[7:]
    except IndexError: return
    with open("playing.txt", 'w') as outfile:
        json.dump(PLAYING, outfile)
    chat(ws, "%s play list updated: %s" % (username, PLAYING[username]), channelID)

def whoPlays(ws, text, channelID):
    users = []
    try: game = text[10:]
    except IndexError: return
    for user, games in PLAYING.items():
        if games.find(game) > -1: users.append(user)
    if len(users) == 1:
        chat(ws, "%s plays %s" % (', '.join(users), game), channelID)
    elif len(users) > 1:
        chat(ws, "%s all play %s" % (', '.join(users), game), channelID)
    else:
        chat(ws, "Sorry, nobody plays %s" % game, channelID)

def getPlaying(ws, userID, text, channelID):
    try: username = text.split(' ')[1]
    except IndexError: return
    try: games = PLAYING[username]
    except KeyError: games = None
    if games == None:
        chat(ws, "sorry, %s hasn't shared what games they're playing." % username, channelID)
    else:
        chat(ws, "%s is currently playing: %s" % (username, games), channelID)

def getQuote(ws, channelID):
    chat(ws, QUOTES[random.randrange(len(QUOTES))], channelID)

def suggestGame(ws, channelID):
    gameDict = {}
    for user, games in PLAYING.items():
        for eachGame in games.split(' '):
            gameDict[eachGame] = True
    games = gameDict.keys()
    chat(ws, "you might try %s" % games[random.randrange(len(games))], channelID)

def adjustDKP(ws, userID, text, channelID):
    info = text.split(' ')
    try: username = info[1]
    except IndexError: return
    if text[0] == '+':
        try: num = int(info[0][1:])
        except:
            chat(ws, "maths are hard, no thanks.", channelID)
            return
        if username in DKP:
            DKP[username] = DKP[username] + num
        else:
            DKP[username] = num
    if text[0] == '-':
        try: num = int(info[0][1:])
        except:
            chat(ws, "maths are hard, no thanks.", channelID)
            return
        if username in DKP:
            DKP[username] = DKP[username] - num
        else:
            DKP[username] = num
    with open("DKP.txt", 'w') as outfile:
        json.dump(DKP, outfile)
    chat(ws, "%s's DKP total has been adjusted. Their new total is: %d" % (username, DKP[username]), channelID)

def getJoke(ws, channelID):
    chat(ws, JOKES[random.randrange(len(JOKES))], channelID)

def roll(ws, userID, text, channelID):
    request = text.split(' ')
    if len(request) > 1:
        try:
            dice = request[1]
            details = dice.split('d')
            times = details[0]
            size = details[1]
            additive = size.split('+')
            bonus = 0
            if len(additive) > 1:
                size = additive[0]
                bonus = int(additive[1])
            subs = size.split('-')
            if len(subs) > 1:
                size = subs[0]
                bonus = 0 - int(subs[1])
            total = 0
            for i in range(int(times)):
                total = total + random.randrange(int(size)) + 1
            total = total + bonus
            chat(ws, "%s rolled %s" % (getUserName(userID), str(total)), channelID)
        except:
            chat(ws, "I'm sorry but I don't understand '%s'" % request[1], channelID)
    else:
        chat(ws, "%s rolled %s" % (getUserName(userID), str(random.randrange(10000))), channelID)

	#prints the list of commands in the specified channel (we use a designated spam channel in this example but it can be changed easily)
def sendHelp(ws, userID, channelID):
    chat(ws, "Check the spam channel (the list is pretty long).", channelID)
    chat(ws, "Commands to the dragon are as follows:\n  !flame username -- will taunt user\n  !praise username -- will praise user\n  !pic search_string -- will display a random picture after searching Bing for search_string\n  !iplay game1 game2 game3 -- will record that you are playing game1 game2 game3\n  !whoplays game -- will list all people who have reported that they play game\n  !playing name -- will list every game name is playing\n  !quote -- put up a random quote\n  !suggest game -- will choose a game from the list of all games people are playing\n  +amount name -- assign amount DKP to name\n  -amount name -- remove amount DKP from name\n  !joke -- offer a random joke\n  !roll -- return a random number between 0 and 10000\n  !stock (name/symbol) -- get the current quote for ticker\n  !coin coinname -- get the current price of cryptocurrency <coin>\n  !record username -- record the last thing username said.\n  !test -- make sure the bot is responding.", getChannelID("spam"))

def stockCheck(ws, userID, text, channelID):
    info = text.split(' ')
    if len(info) < 2: return
    item = info[1]
    quoteURL = "http://finance.yahoo.com/q?s=" + item
    infile = urllib.request.urlopen(quoteURL)
    data = infile.readall().decode('utf-8')
    infile.close()
    matches = re.findall("class=\"time_rtq_ticker\">.*?>(.*?)</span>", data)
    if len(matches) == 0:
        chat(ws, "I'm sorry but I couldn't find any information about %s" % ' '.join(info[1:]), channelID)
    else:
        chat(ws, "Current spot price of %s: $%s" % (item, matches[0]), channelID)

def coinPrice(ws, userID, text, channelID):
    info = text.split(' ')
    if len(info) < 2: return
    item = info[1]
    infile = urllib.request.urlopen("http://coinmarketcap.com")
    data = infile.readall().decode('utf-8')
    infile.close()
    matches = re.findall("<tr id=\"id-" + item + ".*?</tr>", data, re.S)
    if len(matches) == 0:
        chat(ws, "I'm sorry, but I couldn't find any information about %s" % ' '.join(info[1:]), channelID)
    else:
        data = matches[0]
        marketCap = re.findall("market-cap.*?data-usd=\"(.*?)\"", data)
        price = re.findall("class=\"price\" data-usd=\"(.*?)\"", data)
        volume = re.findall("class=\"volume\" data-usd=\"(.*?)\"", data)
        percent = re.findall("percent-24h.*?data-usd=\"(.*?)\"", data)
        if len(price) == 0:
            chat(ws, "I'm sorry, but I couldn't find any information about %s" % ' '.join(info[1:]), channelID)
            return
        else: price = price[0]
        if len(marketCap) == 0: marketCap = "?"
        else: marketCap = marketCap[0]
        if len(volume) == 0: volume = "?"
        else: volume = volume[0]
        if len(percent) == 0: percent = "?"
        else: percent = percent[0]
        chat(ws, item + " price: $%s, change: %%%s, volume: $%s, market cap: $%s" % (price, percent, volume, marketCap), channelID)

def recordQuote(ws, userID, text, channelID):
    info = text.split(' ')
    if len(info) < 2: return
    target = info[1]
    if target not in RECENT_MESSAGES:
        chat(ws, target + " hasn't said anything recently, sorry.", channelID)
        return
    quote = RECENT_MESSAGES[target]
    outfile = open("quotes.txt", 'a')
    outfile.write(quote + " -- " + target + '\n')
    outfile.close()
    QUOTES.append(quote + " -- " + target)
    chat(ws, quote + " -- " + target + " recorded.", channelID)

#not yet fully implemented.
'''def urbanDefine(ws, text, channelID):
    chat(ws, "You'll have to look it up yourself for now.", channelID) '''

def dragonTest(ws, text, channelID):
    chat(ws, "I'm here!", channelID)
	
def playRPS(ws, text, channelID):
    chat(ws, "%s" % (RPS[random.randrange(len(RPS))]), channelID)

def onError(ws, error):
    print("ERROR:\n" + error)

def onClose(ws):
    print("closing now.")

if __name__ == "__main__":
    try:
        with open("playing.txt") as infile:
            PLAYING = json.load(infile)
    except IOError: PLAYING = {}
    try:
        with open("DKP.txt") as infile:
            DKP = json.load(infile)
    except IOError: DKP = {}
	
wsURL = authenticateDragon()
websocket.enableTrace(True)
ws = websocket.WebSocketApp(wsURL, on_message = onMessage, on_error = onError, on_close = onClose)
ws.run_forever(ping_interval=60)
