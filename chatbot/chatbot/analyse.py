from dandelion import DataTXT
from textblob import TextBlob
import nltk
import discordIntergration
from textblob import Word
from textblob.wordnet import *

import database
#from nltk.corpus import *
#print((os.path.join('Project2/spelregels.bmp')))

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