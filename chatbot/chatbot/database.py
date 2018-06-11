import discord
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Date
from sqlalchemy.sql.expression import func
from sqlalchemy import update

import _datetime as datetime

import analyse

Base = declarative_base()
engine = create_engine('sqlite:///messages.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

def getDBSession():
    return DBSession()

class Message(Base):
    __tablename__ = 'Message'
    id = Column(Integer, primary_key=True) 
    sender = Column(String(50), primary_key=True)
    keyword = Column(String(500), primary_key=True)
    frequency = Column(Integer)
    lastDate = Column(Date)
    recommendation = Column(Float)

def createTablesDB():
    Base.metadata.create_all(engine)

def getId(session):
    qry = session.query(func.max(Message.id))
    id = qry.one()[0]    
    if id == None:
        return 0
    return id + 1

#puts the message in the database
def addMessageToDB(message, keywords):
    for i in range(0, len(keywords)):
        try:
            session = DBSession()
            sender = message.author.name
            keyword = keywords[i].title
            date = datetime.datetime.now()
            messages = session.query(Message).all()
            add = True;
            for i in range(0, len(messages)):
                mess = messages[i]
                if(mess.sender == sender and mess.keyword == keyword):
                    add = False
                    freq = mess.frequency + 1
                    newScore = analyse.updateScoreMessage(message, mess)
                    session.query(Message).filter_by(id=mess.id).update({"frequency":freq, "recommendation":newScore})
                    session.commit()
            if(add):
                id=getId(session)
                m = Message(id=id, sender=sender, keyword=keyword, frequency=1, lastDate=date, recommendation=50.0)
                session.add(m)
                session.commit()
            session.close()
        except:
            print(message.author.name + ": " + message.content)

#called when a message is received to further process it.
def ReceivedMessage(message):
    print("received a message from " + message.author.name)
    keywords = load_keywords()
    words = message.content.lower().split(" ")
    for i in range(0, len(words)):
        if words[i] in keywords:       #if the message contains a keyword add to db
            addMessageToDB(message)
            print("message saved")
            break

def GetAllAuthorsWith(keyword=None):
    messages = GetAllMessagesWith(keyword)
    if messages=="No people with relevant experience found, please consult the documentation or a manager":
        return messages
    ret = []
    if not keyword == None:
        for i in range(0, len(messages)):
            ret.append(messages[i].sender)

        if ret == []:
            return("No people with relevant experience found, please consult the documentation or a manager")
        return ret
    return messages

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

def GetTopAuthorWith(keyword):
    messages = GetAllMessagesWith(keyword)
    if messages == "No people with relevant experience found, please consult the documentation or a manager":
        return messages
    best = messages[0]
    for i in range(1,len(messages)):
        m = messages[i]
        if i == 0:
            best = m
        else:
            if(m.recommendation > best.recommendation):
                best = m
    return best.sender
