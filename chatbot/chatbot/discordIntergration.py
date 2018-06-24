import discord
import userInput
import database
import analyse
from chatterbot import ChatBot
import _datetime as datetime
from database import addLog

currentlog = ""

#logs a message to the current log
def log(message):
    file = open(currentlog, "a")
    file.write(message + "\n")
    file.close()



bot = ChatBot("Liabeter2", trainer='chatterbot.trainers.UbuntuCorpusTrainer')
#bot.train()
client = discord.Client()
client.logout()
client.close()


#function that triggers on the event on_message, telling the bot to read the message
@client.event
async def on_message(message):
    # don't react to own messages
    if message.author == client.user:
        return

    print("Message received from {0}".format(message.author.name))
    message.content = message.content.lower()
    print(message.content)
    addLog(str(message.author.name), str(message.content))

    resultString = ""
    feedbackString = ""
    if not message.channel.is_private and not ("<@&446757834093494272>" in message.content or "<@458635950428520472>" in message.content):# Lia
   # if not message.channel.is_private and not ("<@&446757834093494272>" in message.content or "<@455668662066741250>" in message.content): #pj78 bot
        try:
            keyword1 = analyse.APIrequester(message.content)
            keywords = keyword1['keywords']
            if(len(keywords) > 0):
                database.addMessageToDB(message, keywords)
                console.writeline("Found keyword(s) in last message.")
                addLog("Bot", "Found keyword(s) in last message.")
        except:
            resultString = ""
    else:
        if message.content.startswith("!Feedback"):
            username = ""
            keyword = ""
            rating = ""
            Userstart = False
            Keywordstart = False
            Ratingstart = False
            i = 0
            while i < len(message.content):
                if message.content[i] == ':':
                    if message.content[i+1] == ' ':
                            i += 1
                    Userstart = True
                elif Userstart:
                    if message.content[i] == ',':
                        if message.content[i+1] == ' ':
                            i += 1
                        Keywordstart = True
                        Userstart = False
                    else:
                        username += message.content[i]
                elif Keywordstart:
                    if message.content[i] == ',':
                        if message.content[i+1] == ' ':
                            i += 1
                        Ratingstart = True
                        Keywordstart = False
                    else:
                        keyword += message.content[i]
                elif Ratingstart:
                    rating += message.content[i]
                i += 1
            floatrating = None
            try:
                floatrating = float(rating)
                if floatrating > 10.0:
                    floatrating = 10.0
                elif floatrating < 1.0:
                    FloatingPointError = 1.0
                ret = None
                ret = analyse.updateScoreFeedback(username.lower(), keyword.lower(), floatrating)
                if ret == None:
                    resultString = 'Thank you for your feedback on user {username}'.format(username = username)
                else:
                    resultString = ret
            except:
                resultString = "You did something wrong!"
                addLog("Bot", "You did something wrong!")
        else:
            if message.content.startswith("!"):
                try:
                    keyword1 = analyse.APIrequester(message.content[1:])
                    keywords = keyword1['keywords']

                    resultString = "These are the keywords I found in your message and a person that might be able to help you: "
                    for i in range(0,len(keywords)):
                        keyword = keywords[i]
                        author = database.GetTopAuthorWith(keyword, message.author.name.lower())
                        resultString = resultString + "\n" + keyword + ": " + author
        
                except:
                    resultString = ""
           # elif "<@&446757834093494272>" in message.content or "<@455668662066741250>" in message.content: #pj78
            elif "<@&446757834093494272>" in message.content or "<@458635950428520472>" in message.content:#lia
                try:
               
                    keyword1 = analyse.APIrequester(message.content[21:])
                    keywords = keyword1['keywords']

                    resultString = "These are the keywords I found in your message and a person that might be able to help you: "
                    for i in range(0,len(keywords)):
                        keyword = keywords[i]
                        author = database.GetTopAuthorWith(keyword, message.author.name.lower())
                        resultString = resultString + "\n" + keyword + ": " + author

                except:
                    resultString = ""
            else:
                resultString = bot.get_response(message.content)
            if  resultString == "":
                if not ("<@&446757834093494272>" in message.content or "<@458635950428520472>" in message.content):
                    resultString = bot.get_response(message.content)
                else:
                    resultString = "I couldn't find any keywords in your message or there is no information on the keywords."
            elif message.content.startswith("!"):
                feedbackString = "Could you please give me feedback on the help the suggested person(s) gave you?\nPlease format your message like this:\n!Feedback:<username>,<keyword>,<rating from 1.0 - 10.0>"
    if not resultString == "":
        await client.send_message(message.channel, resultString)
        print(resultString)
        addLog("Bot", str(resultString))
        resultString = None
    if not feedbackString == "":
        await client.send_message(message.channel, feedbackString)
        print(feedbackString)
        addLog("Bot", str(feedbackString))
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
    TOKEN = 'NDU4NjM1OTUwNDI4NTIwNDcy.Dgqhlw.KcYdamEg9IeHrVVqyf5DhjsUc2g' #Lia
    #TOKEN = 'NDU1NjY4NjYyMDY2NzQxMjUw.Df_XJw.94MbMvFY8Br9GTtHHFeO_0NTLuI' #p78 bot
    client.run(TOKEN)