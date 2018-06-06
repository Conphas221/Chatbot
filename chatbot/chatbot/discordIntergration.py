import discord
import userInput

client = discord.Client()

#function that triggers on the event on_message, telling the bot to read the message
@client.event
async def on_message(message):
    # don't react to own messages
    if message.author == client.user:
        return

    print("Message received")

    resultString = "Something went wrong while processing your message."

    try:
        keywords = userInput.HandleInputInternal(message)
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
    TOKEN = 'NDQ2NjU0NzEzMDg2MDgzMDcz.Dd8LRg.jQfWV8UclPrVqBwBR19KS9xeugM'
    client.run(TOKEN)