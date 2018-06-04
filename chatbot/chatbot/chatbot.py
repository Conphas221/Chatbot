#imports start
##########################################################################################################################################

import discord

import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import analyse

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

#prints a notification when a message is received
def message(message):
    print('received a message from ' + message.author.name)

#prints a list of messages
def printMessages(messages):
    for i in range(0, len(messages)):
        print(messages[i].sender + ": " + messages[i].content)

#########################################################################################################################################
#functions end

#discordstuff start
##########################################################################################################################################

#function to start discord mode
def discordConnection():
    TOKEN = 'NDQ2NjU0NzEzMDg2MDgzMDcz.Dd8LRg.jQfWV8UclPrVqBwBR19KS9xeugM'
    client.run(TOKEN)
    return client

#function that triggers on the event on_message, telling the bot to read the message
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await ReceivedMessage(message)

#function that triggers on the event on_ready, to tell the user that discord is live
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

#function that calls other functions, only called when user input starts with "-"
def func_caller(command):
	if command == "-k":
		parameter = input("Enter the keywords you want to add to the keyword list, seperated by spaces \n").lower().split(" ") #asks the user for input and split it on space
		keyword_update(parameter,0)
	elif command == "-s":
		display_keywords()
	elif command == "-d":
		remove_keyword_entry()
	elif command == "-b": #entering -b will start the discord bot
		client = discordConnection()
	else:
		print("Command not recognized, try again! \n")

def load_keywords(): #reads the keywords.txt file and returs a list with its content
	try:
		f = open("keywords.txt","r")
		content = f.readlines()
		content = [x.strip() for x in content] 
		f.close()
		return content
	except:
		print("File not found, create a new keyword list with the -k command")

def lookup_matching_employee(inp):
	keys = inp.lower().split(" ")
	return GetAllAuthorsWith(keys)
	#return all users from the database who have send a message that contains at least one of the entries in the keyword list

def remove_keyword_entry():
	keywords_tobe_removed = input("Enter the keywords you want to remove from the keyword list, seperated by spaces \n").lower().split(" ")
	try:
		f = open("keywords.txt","r")
		content = f.readlines()
		content = [x.strip() for x in content]
		for word in keywords_tobe_removed:
			try:
				content.remove(word)
			except:
				print(word+" was not found in the keyword list \n")
		keyword_update(content,1)

		f.close()
	except:
		print("File not found, create a new keyword list with the -k command")

def keyword_update(new_keywords,id): #updates the keyword file, creates it if it doesn't exist.
	if id == 0:
		f = open("keywords.txt","a+") #open the keywords file in append mode, creating a keywords file if it doesn't exist
	else:
		f = open("keywords.txt","w+") #open the keywords file in write mode, creating a keywords file if it doesn't exist
	for word in new_keywords:
		f.write(word+"\n")
	f.close()
	print("update complete")

def display_keywords(): #prints all keywords, handles the file not found error
	try:
		f = open("keywords.txt","r")
		content = f.readlines()
		content = [x.strip() for x in content] 
		for word in content:
			print(word)
		f.close()
	except:
		print("File not found, create a new keyword list with the -k command")

#checks a message for answering it with information
def startLookUp(message):
    inp = ""
    words = message.content.lower().split(" ")
    keywords = load_keywords()
    for i in range(0, len(words)):
        if words[i] in keywords:
            inp += words[i] + " "
    if inp[len(inp)-1] == ' ':
        newInp=""
        for i in range(0,len(inp)-1):
            newInp+=inp[i]
        inp = newInp
    users = lookup_matching_employee(inp)
    if users == "No people with relevant experience found, please consult the documentation or a manager":
        return users
    msg = "These employee(s) might be able to help you:\n"
    for i in range(0, len(users)):
        msg += users[i] + "\n"
    return msg

##########################################################################################################################################
#analyse end

#database start
##########################################################################################################################################

#class Message for the database
class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True) 
    sender = Column(String(50))
    content = Column(String(500))

#function to create a table in the database
def createTablesDB():
    Base.metadata.create_all(engine)

#puts the message in the database
def addMessageToDB(message):
    session = DBSession()
    m = Message(sender=message.author.name, content=message.content)
    session.add(m)
    session.commit()

#called when a message is received to further process it.
async def ReceivedMessage(message):
    print("received a message from " + message.author.name)
    keywords = load_keywords()
    words = message.content.lower().split(" ")
    for i in range(0, len(words)):
        if words[i] in keywords:       
            if(message.channel.is_private):#if the message is send directly to the bot, answer the message
                await client.send_message(message.channel, startLookUp(message))
                break
            else:#if the message contains a keyword add to db
                addMessageToDB(message)
                print("message saved")
                break

#gets all unique authors in the db with a specified keyword in one or more of their messages or all unique authors if no keyword is specified
def GetAllAuthorsWith(keyword=None):
    session = DBSession()
    messages = session.query(Message).all()
    ret = []
    if not keyword == None:
        for i in range(0, len(messages)):
            m = messages[i]
            words = m.content.lower().split(" ")
            not_matched = False
            for j in range(0, len(keyword)):
                if keyword[j] not in words:
                    not_matched = True
            if not not_matched:
                if not m.sender in ret:
                    ret.append(m.sender)

        if ret == []:
            return "No people with relevant experience found, please consult the documentation or a manager"
        return ret
    return messages

#gets all unique messages in the db with a specified keyword or all messages if no keyword is specified
def GetAllMessagesWith(keyword=None):
    session = DBSession()
    messages = session.query(Message).all()
    ret = []
    retcheck = []
    if not keyword == None:
        for i in range(0, len(messages)):
            m = messages[i]
            #print(m.sender + ": " + m.content)
            words = m.content.lower().split(" ")
            not_matched = False
            for j in range(0, len(keyword)):
                if keyword[j] not in words:
                    not_matched = True
            if not not_matched:
                if not m.content in retcheck:
                    ret.append(m)
                    retcheck.append(m.content)


        if ret == []:
            print("No people with relevant experience found, please consult the documentation or a manager")
        return ret
    return messages

##########################################################################################################################################
#database end


#main program start
##########################################################################################################################################

# Define main() function
def main():
	loop = True
	print("use the -k command to add entries to the keyword list"+"\n"+"use the -s command to print all keywords"+"\n"+"use the -d command to delete keywords from the list"+"\nuse the -b command to enter discord bot mode"+"\nEnter a keyword to look up users with relevant experience")
	while loop:
		user_input = input().lower()
		#if user_input[:1] != "-":
		#	lookup_matching_employee(user_input)
		#else:
			#func_caller(user_input[:2])
		annotations = analyse.AnalyseText(user_input)
		for a in annotations:
		    print(a.spot)

#printMessages(GetAllMessagesWith())
#createTablesDB()
main()

##########################################################################################################################################
#main program end