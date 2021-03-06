#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
from sqlalchemy import Column, String, Integer, DateTime
from pipobot.lib.bdd import Base


class RepostUrl(Base):
    __tablename__ = "url"
    url = Column(String(250), primary_key=True)
    count = Column(Integer)
    date = Column(DateTime)
    jid = Column(String(250))
    chan = Column(String(250))

    def __init__(self, url, jid, chan):
        self.url = url
        self.jid = jid
        self.count = 1
        self.date = datetime.datetime.now()
        self.chan = chan
