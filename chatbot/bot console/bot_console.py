from .chatbot import chatbot
import _datetime as datetime
while True:
    date = datetime.datetime.now()
    if date.hour == 19 and date.minute == 37 and date.second == 0:
        messages = database.GetAllMessagesWith()
        for i in range(0,len(messages)):
            analyse.updateScoreTime(messages[i], date)