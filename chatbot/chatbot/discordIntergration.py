import discord
import userInput
import database
import analyse
from chatterbot import ChatBot
import _datetime as datetime

currentlog = ""

#logs a message to the current log
def log(message):
    file = open(currentlog, "a")
    file.write(message + "\n")
    file.close()

bot = ChatBot("project7-8 bot", trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
#bot.train("chatterbot.corpus.english")
client = discord.Client()

#function that triggers on the event on_message, telling the bot to read the message
@client.event
async def on_message(message):
    # don't react to own messages
    if message.author == client.user:
        return

    print("Message received from {0}".format(message.author.name))
    print(message.content)
    log(str(message.author.name + ": " + message.content))

    resultString = ""
    feedbackString = ""
    if not message.channel.is_private and not ("<@&446757834093494272>" in message.content or "<@455668662066741250>" in message.content):
        try:
            keywords = userInput.HandleInputInternal(message.content)
            if(len(keywords) > 0):
                database.addMessageToDB(message, keywords)
                console.writeline("Found keyword(s) in last message.")
                log("Bot: Found keyword(s) in last message.")
        except:
            resultString = ""
    else:
        if message.content.startswith("!Feedback"):
            j = 0
            username = ""
            keyword = ""
            rating = ""
            userDone = False
            keywordDone = False
            for i in range(0, len(message.content)):
                if message.content[i] == ':':
                    j = i + 2
                if i >= j and not userDone and not j == 0:
                    if not message.content[i] == ',':
                        username += message.content[i]
                    else:
                        userDone = True
                        j = 0
                elif i >= j and not keywordDone and not j == 0:
                    if not message.content[i] == ',':
                        keyword += message.content[i]
                    else:
                        keywordDone = True
                        j = 0
                elif i >= j and not j == 0:
                    rating += message.content[i]
            floatrating = None
            try:
                floatrating = float(rating)
                if floatrating > 10.0:
                    floatrating = 10.0
                elif floatrating < 1.0:
                    FloatingPointError = 1.0
                ret = None
                ret = analyse.updateScoreFeedback(username.lower(), keyword, floatrating)
                if ret == None:
                    resultString = 'Thank you for your feedback on user {username}'.format(username = username)
                else:
                    resultString = ret
            except:
                resultString = "You did something wrong!"
                log("Bot: You did something wrong!")
        else:
            if message.content.startswith("!"):
                try:
                    keywords = userInput.HandleInputInternal(message.content[1:])
                    resultString = "These are the keywords I found in your message and a person that might be able to help you: "
                    for keyword in keywords:
                        title = keyword.title
                        author = database.GetTopAuthorWith(title, message.author.name.lower())
                        resultString = resultString + "\n" + keyword.title + ": " + author
                except:
                    resultString = ""
            elif "<@&446757834093494272>" in message.content or "<@455668662066741250>" in message.content:
                try:
                    keywords = userInput.HandleInputInternal(message.content)
                    resultString = "These are the keywords I found in your message and a person that might be able to help you: "
                    for keyword in keywords:
                        title = keyword.title
                        author = database.GetTopAuthorWith(title, message.author.name.lower())
                        resultString = resultString + "\n" + keyword.title + ": " + author
                except:
                    resultString = ""
            else:
                resultString = bot.get_response(message.content)
            if resultString == "These are the keywords I found in your message and a person that might be able to help you: " or resultString == "":
                if not ("<@&446757834093494272>" in message.content or "<@455668662066741250>" in message.content):
                    resultString = bot.get_response(message.content)
                else:
                    resultString = "I couldn't find any keywords in your message or there is no information on the keywords."
            elif message.content.startswith("!"):
                feedbackString = "Could you please give me feedback on the help the suggested person(s) gave you?\nPlease format your message like this:\n!Feedback User: <username>, Keyword: <keyword>, Rating: <rating from 1.0 - 10.0>"
    if not resultString == "":
        await client.send_message(message.channel, resultString)
        print(resultString)
        log("Bot: " + str(resultString))
        resultString = None
    if not feedbackString == "":
        await client.send_message(message.channel, feedbackString)
        print(feedbackString)
        log("Bot: " + str(feedbackString))
        feedbackString = None

#function that triggers on the event on_ready, to tell the user that discord is live
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#function to start discord mode
def main():
    # debug printing
    print("Starting discord bot...")

    global currentlog
    currentlog = str(datetime.datetime.now())[:-7] + ".txt"

    newlog = ""
    for c in currentlog:
        if not c == '-' and not c == ':':
            newlog += c
    currentlog = newlog

    file = open(currentlog, "w")
    file.write("Log started\n")
    file.close()

    # run discord bot
    TOKEN = 'NDU1NjY4NjYyMDY2NzQxMjUw.Df_XJw.94MbMvFY8Br9GTtHHFeO_0NTLuI'
    client.run(TOKEN)