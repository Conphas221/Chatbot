import analyse
import database

# Function that handles the user input internally
def HandleInputInternal(userInput):
    # analyse the text and return the analysed data
    keywords = analyse.AnalyseText(userInput)
    return keywords

def HandleInput(userInput):
    keywords = HandleInputInternal(userInput)
    for keyword in keywords:
        print("Keyword :", keyword.spot, "\n Categories:", keyword.categories,"\n")

def HandleInputInternalneural(userInput):
    # analyse the text and return the analysed data
    keywords = analyse.APIrequester(userInput)
    return keywords

def HandleInputneural(userInput):
    keywords = HandleInputInternal(userInput)
    for keyword in keywords:
        print("Keyword :", keyword.spot, "\n Categories:", keyword.categories,"\n")
