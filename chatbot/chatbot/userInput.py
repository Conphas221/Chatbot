import analyse

# Function that handles the user input internally
def HandleInputInternal(userInput):
    # analyse the text and return the analysed data
    keywords = analyse.AnalyseText(userInput)
    return keywords

def HandleInput(userInput):
    # 
    keywords = HandleInputInternal(userInput)
    for keyword in keywords:
        print(keyword.title)
