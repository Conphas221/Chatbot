from dandelion import DataTXT
from textblob import TextBlob
import nltk
import discordIntergration
from textblob import Word
import userInput
#from textblob.wordnet import *

import database
#from nltk.corpus import *

#nltk.download()#voor de download van nltk corpora

#needs to be given a textblob text
def IsQuestion(text):
    if ("?" in text):
        return True               
    return False


def AnalyseText(text):
    datatxt = DataTXT(app_id='cd32413268454e19a31776d33b5f0ba0', app_key='cd32413268454e19a31776d33b5f0ba0')
    response = datatxt.nex(text,include="categories")

    return response.annotations


def sentiment(text):
    text2 = TextBlob(text)
    #print (text2.sentiment)
    return text2.polarity
    
def wordnet(text):
    #word = Word("octopus")
    #word.get_synsets
    #print (word)
    syns =Word(text)
    print(syns.lemmatize())
    #print(syns[0].lemmas()[0].name())
    #Word("octopus").definition
    #print(syns[0].definition())
    try:
        print(syns.detect_language())
    except:
         print("Text must contain at least 3 characters in order to detect language.")

def updateScoreMessage(message, Message):
    currentscore = Message.recommendation
    scoreModifier = 1 - (currentscore/100)
    if (Message.frequency + 1) % 10 == 0:
        currentscore += 1 * scoreModifier
    if sentiment(message.content) >= 0:
        currentscore += 5 * scoreModifier
    else:
        currentscore -= 5 * scoreModifier
    if currentscore > 100.0:
        currentscore = 100.0
    return round(currentscore, 3)

def updateScoreFeedback(username, keyword, rating):
    dbentry = None
    try:
        messages = database.GetAllMessagesWith(keyword)
        for m in messages:
            if m.sender == username:
                dbentry = m
    except:
        try:
            keywords = AnalyseText(keyword)
            messages = database.GetAllMessagesWith(keywords[0].title)
            for m in messages:
                if m.sender == username:
                    dbentry = m
        except:
            try:
                keywords = wordnet(keyword)
                messages = database.GetAllMessagesWith(keywords[0].title)
                for m in messages:
                    if m.sender == username:
                        dbentry = m
            except:
                return "The combination of User {0} and Keyword {1} could not be found".format(username, keyword)
    if dbentry==None:
        return "The combination of User {0} and Keyword {1} could not be found".format(username, keyword)
    currentscore = dbentry.recommendation
    scoreModifier = 1 - (currentscore/100)
    addscore = rating - 5.5
    currentscore += addscore * scoreModifier
    if currentscore > 100.0:
        currentscore = 100.0
    try:
        session = database.getDBSession()
        session.query(database.Message).filter_by(id=dbentry.id).update({"recommendation":currentscore})
        session.commit()
        session.close()
    except:
        None