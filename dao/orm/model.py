class Topic(db.Model):
    tablename = 'topic'
    topic_name = db.Column(db.String(20), primary_key=True)


associations = db.Table('associate_table',
    db.Column("left_name", db.String(20), db.ForeignKey("presentation.presentation_name"), primary_key=True),
    db.Column("right_name", db.String(20), db.ForeignKey("topic.topic_name"), primary_key=True))



class User(db.Model):
    tablename = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(20), unique=True)
    user_name = db.Column(db.String(20))
    user_phone = db.Column(db.String(20))
    user_birthday = db.Column(db.Date)
    active = db.Column(db.Boolean(), nullable=True)

    user_presentation = db.relationship('Presentation')


class Presentation(db.Model):
    __tablename__ = 'presentation'
    presentation_name = db.Column(db.String(20), primary_key=True)
    presentation_date = db.Column(db.Date)

    user_email = db.Column(db.String(20), db.ForeignKey('user.user_email'))
    topic = db.relationship("Topic", secondary=associations, backref=db.backref('presentations', lazy='dynamic'))
    participant_list_fk = db.relationship("Participant")

class Participant(db.Model):
    __tablename__ = 'participant'
    participant_list = db.Column(db.String(20), primary_key=True)
    participant_name = db.Column(db.String(100))
    presentation_name = db.Column(db.String(20), db.ForeignKey("presentation.presentation_name"), primary_key=True)
