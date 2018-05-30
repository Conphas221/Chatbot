#imports start
##########################################################################################################################################

import discord

import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

##########################################################################################################################################
#imports end

#variables start
##########################################################################################################################################

client = discord.Client()
Base = declarative_base()
engine = create_engine('sqlite:///messages.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

##########################################################################################################################################
#variables end

#functions start
##########################################################################################################################################

#puts the message in the database
def addMessageToDB(message):
    session = DBSession()
    m = Message(sender=message.author.name, content=message.content)
    session.add(m)
    session.commit()

#called when a message is received to further process it.
def ReceivedMessage(message):
    print("recieved a message from " + message.author.name)
    addMessageToDB(message)

#########################################################################################################################################
#functions end

#discordstuff start
##########################################################################################################################################

def discordConnection():
    TOKEN = 'NDQ2NjU0NzEzMDg2MDgzMDcz.Dd8LRg.jQfWV8UclPrVqBwBR19KS9xeugM'
    client.run(TOKEN)
    return client

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    ReceivedMessage(message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

##########################################################################################################################################
#discordstuff end

#analyse start
##########################################################################################################################################



##########################################################################################################################################
#analyse end

#database start
##########################################################################################################################################

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True) 
    sender = Column(String(50))
    content = Column(String(500))

def createTablesDB():
    Base.metadata.create_all(engine)

##########################################################################################################################################
#database end


#main program start
##########################################################################################################################################

#createTablesDB()

client = discordConnection()


##########################################################################################################################################
#main program end