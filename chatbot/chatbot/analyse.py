from dandelion import DataTXT
from textblob import TextBlob
import nltk
import discordIntergration
from textblob import Word
from textblob.wordnet import *
#from nltk.corpus import *

#nltk.download()#for de download van nltk corpora



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
