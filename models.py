from getSauce import db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class users(db.Model, base):
    username = db.Column("username", db.String(10), primary_key=True)
    password = db.Column("password", db.String(16))
    email = db.Column("email", db.String(20))
    child = relationship("results", uselist=False, back_populates="parent")


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class results(db.Model, base):
    username = db.Column("username", db.String(10), ForeignKey('users.username'))
    resulttitle = db.Column("resulttitle", db.String(16))
    date = db.Column("date", DateTime(), primary_key=True)
    parent = relationship("users", back_populates="child")

    def __init__(self, username, resulttitle, date):
        self.username = username
        self.resulttitle = resulttitle
        self.date = date


