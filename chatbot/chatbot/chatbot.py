import time
import _datetime as datetime
import analyse
from analyse import APIrequester
import discordIntergration
import userInput
import database
from textblob import TextBlob
import nltk
import requests
from requests.adapters import HTTPAdapter
import json
import os
import os.path as path
import threading



#nltk.download('punkt')
#nltk.download('wordnet')
# Command class

class Command:
    def __init__(self, command, callback):
        self.command = command
        self.callback = callback

    def GetCommand(self):
        return self.command

    def GetCallback(self):
        return self.callback

# Command array
commands = []

# Adds a command to the command handler
def RegisterCommand(command, callback):
    cmd = Command(command, callback)
    commands.append(cmd)

# Run a defined command, or return false if it does not exist
def RunCommand(command, args):
    for cmd in commands:
        if cmd.GetCommand() == command:
            cmd.GetCallback()(args)
            return True

    return False
 

def startapi():
    os.chdir("../api")

    import subprocess
    from subprocess import Popen
    subprocess.run("node index.js", shell=True)
    
    
   




    


# Define main() function
def main():
    # Register commands
    RegisterCommand("-b", lambda args : threading.Thread(target = discordIntergration.main).start())
    RegisterCommand("quit", lambda args : exit())
    RegisterCommand("-r", lambda args : threading.Thread(target = startapi).start())




    print("use the -b command to enter discord bot mode"+"\nEnter a keyword to look up users with relevant experience")

    # Command loop
    while True:
        date = datetime.datetime.now()
        if(date.hour == 19 and date.minute == 50 and date.second == 0):
            messages = database.GetAllMessagesWith()
            for i in range(0, len(messages)):
                analyse.updateScoreTime(messages[i], date)
        # Obtain the user input from the command line
        user_input = input().lower()
        blob = TextBlob(user_input) #creates a textblob variable of the input


        # Run a command, if the command is not found, analyse the user input
        if (RunCommand(user_input, user_input) == False) and (blob.words != []): #makes sure HandleInput is not passed null or empty
           #userInput.HandleInput(user_input)
           analyse.APIrequester(user_input)
           # print(user_input)
           #analyse.wordnet(user_input)

# run the main function
main()


