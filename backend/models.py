import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

#Setting environment variables for accessing Postgres database.
os.environ.setdefault('database_user','student')
os.environ.setdefault('database_password','')
os.environ.setdefault('database_host','localhost')
os.environ.setdefault('database_port','5432')
os.environ.setdefault('database_name','trivia')
    #Sources: https://stackoverflow.com/questions/5971312/how-to-set-environment-variables-in-python
    #       : https://stackoverflow.com/questions/4906977/how-can-i-access-environment-variables-in-python

database_path = 'postgresql://{}:{}@{}:{}/{}'.format(os.environ['database_user']
                                                    ,os.environ['database_password']
                                                    ,os.environ['database_host']
                                                    ,os.environ['database_port']
                                                    ,os.environ['database_name'])
    #High-level database path structure: 'dialect+driver://username:password@host:port/database'
    #Source: https://campus.datacamp.com/courses/introduction-to-relational-databases-in-python/applying-filtering-ordering-and-grouping-to-queries?ex=2#:~:text=You%20might%20recall%20from%20Chapter%201%20that%20we,In%20general%2C%20connection%20strings%20have%20the%20form%20%22dialect%2Bdriver%3A%2F%2Fusername%3Apassword%40host%3Aport%2Fdatabase%22

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

"""
Question

"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }

"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }
