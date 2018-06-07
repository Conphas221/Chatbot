#import discord


import analyse
import discordIntergration
import userInput
import database

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

# Define main() function
def main():
    # Register commands
    RegisterCommand("-b", lambda args : discordIntergration.main())
    RegisterCommand("-k", lambda args : None)
    RegisterCommand("-s", lambda args : None)
    RegisterCommand("-d", lambda args : None)
    RegisterCommand("quit", lambda args : exit())

    print("use the -k command to add entries to the keyword list"+"\n"+"use the -s command to print all keywords"+"\n"+"use the -d command to delete keywords from the list"+"\nuse the -b command to enter discord bot mode"+"\nEnter a keyword to look up users with relevant experience")

    # Command loop
    while True:
        # Obtain the user input from the command line
        user_input = input().lower()

        # Run a command, if the command is not found, analyse the user input
        if (RunCommand(user_input, user_input) == False):
            userInput.HandleInput(user_input)

# run the main function
main()
