#imports start
##########################################################################################################################################

import discord

##########################################################################################################################################
#imports end

#discordstuff start
##########################################################################################################################################


#def discordConnection():
#    TOKEN = 'NDQ2NjU0NzEzMDg2MDgzMDcz.Dd8LRg.jQfWV8UclPrVqBwBR19KS9xeugM'
#    client = discord.Client()
#    client.run(TOKEN)
#    return client
#client = discordConnection()

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#    chatbot.message(message)

#@client.event
#async def on_ready():
#    print('Logged in as')
#    print(self.client.user.name)
#    print(self.client.user.id)
#    print('------')

##########################################################################################################################################
#discordstuff end

#analyse start
##########################################################################################################################################



##########################################################################################################################################
#analyse end

#database start
##########################################################################################################################################



##########################################################################################################################################
#database end


#main program start
##########################################################################################################################################






#function that calls other functions, only called when user input starts with "-"
def func_caller(command):
	if command == "-k":
		parameter = input("Enter the keywords you want to add to the keyword list, seperated by spaces \n").split(" ") #aks the user for input and split it on space
		keyword_update(parameter,0)
	elif command == "-s":
		display_keywords()
	elif command == "-d":
		remove_keyword_entry()


def lookup_matching_employee(inp):
	keys = inp.split(" ")
	print("Not implemented yet!")
	#return all users from database who match at least one of the entries in the keys list

def remove_keyword_entry():
	keywords_tobe_removed = input("Enter the keywords you want to remove from the keyword list, seperated by spaces \n").split(" ")
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

def message(message):
    print('received a message from ' + message.author.name)


# Define main() function
def main():
	loop = True
	print("use the -k command to add entries to the keyword list"+"\n"+"use the -s command to print all keywords"+"\n"+"use the -d command to delete keywords from the list")
	while loop:
		user_input = input()
		if user_input[:1] != "-":
			lookup_matching_employee(user_input)
		else:
			func_caller(user_input[:2])



main()

##########################################################################################################################################
#main program end