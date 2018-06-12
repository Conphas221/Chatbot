import _datetime as datetime
from .chatbot import *

import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Date
from sqlalchemy.sql.expression import func
from sqlalchemy import update
Base = declarative_base()
engine = create_engine('sqlite:///D:/Users/Van Ek/Documents/studie/project 7-8/github/Chatbot/chatbot/chatbot/messages.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
print("start")

class Message(Base):
    __tablename__ = 'Message'
    id = Column(Integer, primary_key=True) 
    sender = Column(String(50), primary_key=True)
    keyword = Column(String(500), primary_key=True)
    frequency = Column(Integer)
    lastDate = Column(Date)
    recommendation = Column(Float)

def updateScoreTime(Message, date):
    print(str(Message.id) + ": " + str(date))
    currentscore = Message.recommendation
    scoreModifier = 1 - (currentscore / 100)
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

def GetAllMessagesWith(keyword=None):
    session = DBSession()
    messages = session.query(Message).all()
    ret = []
    if not keyword == None:
        for i in range(0, len(messages)):
            m = messages[i]
            if(m.keyword == keyword):
                ret.append(m)
        if ret == []:
            return "No people with relevant experience found, please consult the documentation or a manager"
        return ret
    return messages

while True:
    date = datetime.datetime.now()
    if date.hour == 14 and date.minute == 32 and date.second == 0:
        messages = database.GetAllMessagesWith()
        for i in range(0,len(messages)):
            analyse.updateScoreTime(messages[i], date)