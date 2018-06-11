from dandelion import DataTXT
from textblob import TextBlob
import nltk
import discordIntergration
from textblob import Word
from textblob.wordnet import *

import database
#from nltk.corpus import *

#nltk.download()#for de download van nltk corpora

#needs to be given a textblob text
def IsQuestion(text):
    question = False
    questionmarker = ["?","how","why","what","where","who"] #array of question indicators
    if ("?" in text) or (", right" in text): #checks for two specific question indicators that the loop has trouble with
        return not question
    for i in range(0,len(text.words)): #compares every word in the given text with the words in the questionmarker array
        for j in range(0,len(questionmarker)):
            if text.words[i] == questionmarker[j]:# or ("?" in text) or (", right" in text):
                return not question #= True
                #break
    return question


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
    print(syns.detect_language())

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

def updateScoreTime(Message, date):
    print(str(Message.id) + ": " + str(date))
    currentscore = Message.recommendation
    scoreModifier = 1 - (currentscore/100)
    if(scoreModifier < 0.1):
        scoreModifier = 0.1
    lastmonth = Message.lastDate.month + (Message.lastDate.year * 12)
    currentmonth = date.month + (date.year * 12)
    updateMessage = False
    if(currentmonth - lastmonth >= 2):
        currentscore -= 1 * scoreModifier
        updateMessage = True
    if updateMessage:
        try:
            session = database.getDBSession()
            session.query(database.Message).filter_by(id=Message.id).update({"recommendation":currentscore})
            session.commit()
            session.close()
        except:
            print("something went wrong whilst updating the recommendation score")