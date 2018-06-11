from dandelion import DataTXT
from textblob import TextBlob
import nltk
import discordIntergration
from textblob import Word
from textblob.wordnet import *

nltk.download('wordnet')



def AnalyseText(text):
    datatxt = DataTXT(app_id='cd32413268454e19a31776d33b5f0ba0', app_key='cd32413268454e19a31776d33b5f0ba0')
    response = datatxt.nex(text,include="categories")

    return response.annotations

<<<<<<< HEAD

#def sentiment(text):
#    text2 = TextBlob(text)
#    print (text2.sentiment)
    

def wordnet(text):
    word = Word(text)
    word.get_synsets
    print (word)

=======
>>>>>>> 3728052f58e836789e2a1ba4832906f62210e977
