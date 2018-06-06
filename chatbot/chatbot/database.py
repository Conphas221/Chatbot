class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True) 
    sender = Column(String(50))
    content = Column(String(500))

def createTablesDB():
    Base.metadata.create_all(engine)

#puts the message in the database
def addMessageToDB(message):
    session = DBSession()
    m = Message(sender=message.author.name, content=message.content)
    session.add(m)
    session.commit()

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
    session = DBSession()
    messages = session.query(Message).all()
    ret = []
    if not keyword == None:
        for i in range(0, len(messages)):
            m = messages[i]
            words = m.content.lower().split(" ")
            not_matched = False
            for j in range(0, len(keyword)):
                if keyword[j] not in words:
                    not_matched = True
            if not not_matched:
                if not m.sender in ret:
                    ret.append(m.sender)

        if ret == []:
            print("No people with relevant experience found, please consult the documentation or a manager")
        return ret
    return messages

def GetAllMessagesWith(keyword=None):
    session = DBSession()
    messages = session.query(Message).all()
    ret = []
    retcheck = []
    if not keyword == None:
        for i in range(0, len(messages)):
            m = messages[i]
            #print(m.sender + ": " + m.content)
            words = m.content.lower().split(" ")
            not_matched = False
            for j in range(0, len(keyword)):
                if keyword[j] not in words:
                    not_matched = True
            if not not_matched:
                if not m.content in retcheck:
                    ret.append(m)
                    retcheck.append(m.content)


        if ret == []:
            print("No people with relevant experience found, please consult the documentation or a manager")
        return ret
    return messages
