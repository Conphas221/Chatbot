import analyse
import database

# Function that handles the user input internally
def HandleInputInternal(userInput):
    # analyse the text and return the analysed data
    keywords = analyse.AnalyseText(userInput.content)
    if(len(keywords) > 0):
        database.addMessageToDB(userInput)
    return keywords

def HandleInput(userInput):
    keywords = HandleInputInternal(userInput)
    for keyword in keywords:
        print("Keyword :", keyword.spot, "\n Categories:", keyword.categories,"\n")
