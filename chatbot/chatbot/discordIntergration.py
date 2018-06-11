import discord
import userInput
import database

client = discord.Client()

#function that triggers on the event on_message, telling the bot to read the message
@client.event
async def on_message(message):
    # don't react to own messages
    if message.author == client.user:
        return

    print("Message received from {0}".format(message.author.name))

    resultString = "Something went wrong while processing your message."

    try:
        keywords = userInput.HandleInputInternal(message.content)
        if(len(keywords) > 0):
            database.addMessageToDB(message, keywords)
        resultString = "Found the following keywords in your message: "

        for keyword in keywords:
            resultString += keyword.spot + ", "
    except:
        None

    await client.send_message(message.channel, resultString)

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

    # run discord bot
    TOKEN = 'NDU1NjY4NjYyMDY2NzQxMjUw.Df_XJw.94MbMvFY8Br9GTtHHFeO_0NTLuI'
    client.run(TOKEN)