from dandelion import DataTXT
from textblob import TextBlob
import nltk
import discordIntergration
from textblob import Word
from textblob.wordnet import *
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
    print (text2.sentiment)
    
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
