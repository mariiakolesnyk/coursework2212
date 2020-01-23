from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from Forms.UserForm import UserForm
from Forms.TopicForm import TopicForm
from Forms.PresentationForm import PresentationForm
from Forms.ParticipantForm import ParticipantForm
from Forms.UserFormEdit import UserFormEdit
from Forms.PresentationFormEdit import PresentationFormEdit
from Forms.TopicFormEdit import TopicFormEdit
from Forms.ParticipantFormEdit import ParticipantFormEdit

from sqlalchemy.sql import func
import plotly
import plotly.graph_objs as go

import json

from Forms.UserForm import UserForm

app = Flask(__name__)
app.secret_key = 'key'

# ENV = 'prod'
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01200120@localhost/Illa'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jqmtgtltfxjxyw:5d4ed79bfdf9814b34a3483aa0bcfd112fae242e1b10692629464e2a72a470ba@ec2-174-129-253-101.compute-1.amazonaws.com:5432/daeiv5k0b4d4pp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Topic(db.Model):
    tablename = 'topic'
    topic_name = db.Column(db.String(20), primary_key=True)


associations = db.Table('associate_table',
    db.Column("left_name", db.String(20), db.ForeignKey("presentation.presentation_name"), primary_key=True),
    db.Column("right_name", db.String(20), db.ForeignKey("topic.topic_name"), primary_key=True))



class User(db.Model):
    tablename = 'user'
    user_email = db.Column(db.String(20), primary_key=True)
    user_name = db.Column(db.String(20))
    user_phone = db.Column(db.String(20))
    user_birthday = db.Column(db.Date)

    user_presentation = db.relationship('Presentation')


class Presentation(db.Model):
    __tablename__ = 'presentation'
    presentation_name = db.Column(db.String(20), primary_key=True)
    presentation_date = db.Column(db.Date)

    user_email = db.Column(db.String(20), db.ForeignKey('user.user_email'))
    participant_list_fk = db.relationship("Participant")
    topic = db.relationship("Topic", secondary=associations, backref=db.backref('presentations', lazy='dynamic'))


class Participant(db.Model):
    __tablename__ = 'participant'
    participant_list = db.Column(db.String(20), primary_key=True)
    participant_name = db.Column(db.String(100))
    presentation_name = db.Column(db.String(20), db.ForeignKey("presentation.presentation_name"), primary_key=True)


# создание всех таблиц
db.create_all()



Maria = User(user_email='maria@gmail.com',
             user_name='Maria',
             user_phone='+380669983855',
             user_birthday="1999-04-07"
             )

Bob = User(user_email = 'bob@gmail.com',
             user_name = 'Bob',
             user_phone = '+380123456789',
             user_birthday = '2000-1-20'
             )

Kate = User(user_email = 'kate@gmail.com',
             user_name = 'Kate',
             user_phone = '+123456789011',
             user_birthday = '1998-2-25'
            )

Alex = User(user_email = 'alex@gmail.com',
             user_name = 'Alex',
             user_phone = '+380999999999',
             user_birthday = '1997-2-25'
            )

Sam = User(user_email = 'sam@gmail.com',
             user_name = 'Sam',
             user_phone = '+380777777777',
             user_birthday = '1999-2-1'
            )


Sales = Presentation(presentation_name = 'Sales',
           presentation_date = '2020-1-4')

DataBase = Presentation(presentation_name = 'DataBase',
                  presentation_date = '2020-1-8'
                  )

Music = Presentation(presentation_name = 'Music',
                     presentation_date = '2020-1-12'
                 )

Maths = Presentation(presentation_name = 'Maths',
                    presentation_date = '2020-1-29'
                    )

Sports = Presentation(presentation_name = 'Sports',
                 presentation_date = '2020-2-1'
                 )

Alex.user_presentation.append(Sales)
Bob.user_presentation.append(DataBase)
Maria.user_presentation.append(Music)
Alex.user_presentation.append(Maths)
Alex.user_presentation.append(Sports)

Science_Maths = Participant(participant_list = 'Science_Maths',
               participant_name = 'Alex, Bob'
               )

Art_Music = Participant(participant_list = 'Art_Music',
             participant_name = 'Maria'
             )

Computer_DataBase = Participant(participant_list = 'Computer_DataBase',
                   participant_name = 'Alex, Bob, Sam'
                   )

Business_Sales = Participant(participant_list = 'Business_Sales',
                participant_name = 'Maria'
                )

Math_Maths = Participant(participant_list = 'Math_Maths',
                participant_name = 'Bob, Sam')

Maths.participant_list_fk.append(Science_Maths)
Sales.participant_list_fk.append(Business_Sales)
Maths.participant_list_fk.append(Math_Maths)

Art = Topic(topic_name = 'Art'
               )
Science = Topic(topic_name = 'Science'
                  )
Math = Topic(topic_name = 'Math'
                )
Computer = Topic(topic_name = 'Computer'
                         )
Business = Topic(topic_name = 'Business'
                   )

Sales.topic.append(Business)
DataBase.topic.append(Computer)
Music.topic.append(Art)
Maths.topic.append(Science)
Maths.topic.append(Math)


db.session.add_all([Alex])

db.session.commit()