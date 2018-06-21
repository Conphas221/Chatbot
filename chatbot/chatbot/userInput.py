import analyse
import database

def APIrequester(message):
    url = "http://localhost:5000/analyse"

    r = requests.post(url, json={"data": message})
    data = r.read()

    print(data)

# Function that handles the user input internally
def HandleInputInternal(userInput):
    # analyse the text and return the analysed data
    keywords = analyse.AnalyseText(userInput)
    api_data = APIrequester(userInput)

    return keywords

def HandleInput(userInput):
    keywords = HandleInputInternal(userInput)
    for keyword in keywords:
        print("Keyword :", keyword.spot, "\n Categories:", keyword.categories,"\n")
