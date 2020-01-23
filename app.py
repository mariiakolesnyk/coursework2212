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

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from math import exp

from flask_security import SQLAlchemyUserDatastore, current_user, login_required, roles_accepted, RoleMixin, UserMixin \
    , Security

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'prod'
# ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01200120@localhost/Illa'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://vkuaifteneantq:05e6bc5aeac65780796b869109dca62f115fc6e97bd66f43ca08361a5723330e@ec2-34-193-42-173.compute-1.amazonaws.com:5432/d6liau6otvc7d8'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['SECURITY_PASSWORD_HASH'] = 'sha256_crypt'
app.config['USER_EMAIL_SENDER_EMAIL'] = "noreply@example.com"

db = SQLAlchemy(app)


class Input_L:
    def activation(self, x):
        self.y = x * 1
        return self.y


class Image_L:
    def __init__(self, w):
        self.w = w

    def activation(self, x):
        sum = 0
        for i in range(len(self.w)):
            sum += exp(-(self.w[i] - x[i]) ** 2 / 0.3 ** 2)
        return sum


class Add_L:
    def activation(self, x):
        sum = 0
        for i in x:
            sum += i
        res = sum / len(x)
        return res


class Output_L:
    def activation(self, x):
        clas = "unpopular"
        val = x[clas]
        for i in x.items():
            if i[1] > val:
                clas = i[0]
        return clas


class Topic(db.Model):
    tablename = 'topic'
    topic_name = db.Column(db.String(20), primary_key=True)


associations = db.Table('associate_table',
                        db.Column("left_name", db.String(20), db.ForeignKey("presentation.presentation_name"),
                                  primary_key=True),
                        db.Column("right_name", db.String(20), db.ForeignKey("topic.topic_name"), primary_key=True))

person_have_role = db.Table('person_have_role',
                            db.Column("user_id", db.Integer(), db.ForeignKey('user.id')),
                            db.Column("role_id", db.Integer(), db.ForeignKey('orm_role.id'))
                            )

class User(db.Model, UserMixin):
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

    roles = db.relationship("ormRole", secondary=person_have_role, backref=db.backref('person', lazy='dynamic'))
    user_presentation = db.relationship('Presentation')

class ormRole(db.Model, RoleMixin):
    __tablename__ = 'orm_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

class Presentation(db.Model):
    __tablename__ = 'presentation'
    presentation_name = db.Column(db.String(20), primary_key=True)
    presentation_date = db.Column(db.Date)
    presentation_link = db.Column(db.String(500))

    user_email = db.Column(db.String(20), db.ForeignKey('user.user_email'))
    topic = db.relationship("Topic", secondary=associations, backref=db.backref('presentations', lazy='dynamic'))
    participant_list_fk = db.relationship("Participant")


class Participant(db.Model):
    __tablename__ = 'participant'
    participant_list = db.Column(db.String(20), primary_key=True)
    participant_name = db.Column(db.String(100))
    presentation_name = db.Column(db.String(20), db.ForeignKey("presentation.presentation_name"), primary_key=True)


user_datastore = SQLAlchemyUserDatastore(db, User, ormRole)
security = Security(app, user_datastore)


# создание всех таблиц


@app.route('/new', methods=['GET', 'POST'])
def new():
    db.create_all()

    Maria = user_datastore.create_user(
        username="Maria",
        password="0000",
        email="maria@gmail.com",
        user_email='maria@gmail.com',
        user_name='Maria',
        user_phone='+380669983855',
        user_birthday="1999-04-07"
    )

    Bob = user_datastore.create_user(
        username="Bob",
        password="0000",
        email="bob@gmail.com",
        user_email='bob@gmail.com',
        user_name='Bob',
        user_phone='+380123456789',
        user_birthday="2000-1-20")

    Kate = user_datastore.create_user(
        username="Kate",
        password="0000",
        email="kate@gmail.com",
        user_email='kate@gmail.com',
        user_name='Kate',
        user_phone='+123456789011',
        user_birthday="1998-2-25")

    Alex = user_datastore.create_user(
        username="Alex",
        password="0000",
        email="alex@gmail.com",
        user_email='alex@gmail.com',
        user_name='Alex',
        user_phone='+380999999999',
        user_birthday="1997-2-25")

    Sam = user_datastore.create_user(
        username="Sam",
        password="0000",
        email="sam@gmail.com",
        user_email='sam@gmail.com',
        user_name='Sam',
        user_phone='+380777777777',
        user_birthday="1999-2-1")

    Admin = user_datastore.create_role(name="Admin")

    User = user_datastore.create_role(name="User")

    Sam.roles.append(User)
    Kate.roles.append(User)
    Alex.roles.append(User)
    Bob.roles.append(User)
    Maria.roles.append(Admin)

    Sales = Presentation(presentation_name='Sales',
                         presentation_date='2020-1-4')

    DataBase = Presentation(presentation_name='DataBase',
                            presentation_date='2020-1-8'
                            )

    Music = Presentation(presentation_name='Music',
                         presentation_date='2020-1-12'
                         )

    Maths = Presentation(presentation_name='Maths',
                         presentation_date='2020-1-29'
                         )

    Sports = Presentation(presentation_name='Sports',
                          presentation_date='2020-2-1'
                          )

    Alex.user_presentation.append(Sales)
    Bob.user_presentation.append(DataBase)
    Maria.user_presentation.append(Music)
    Sam.user_presentation.append(Maths)
    Kate.user_presentation.append(Sports)

    Science_Maths = Participant(participant_list='Science_Maths',
                                participant_name='Alex, Bob'
                                )

    Art_Music = Participant(participant_list='Art_Music',
                            participant_name='Maria'
                            )

    Computer_DataBase = Participant(participant_list='Computer_DataBase',
                                    participant_name='Alex, Bob, Sam'
                                    )

    Business_Sales = Participant(participant_list='Business_Sales',
                                 participant_name='Maria'
                                 )

    Math_Maths = Participant(participant_list='Math_Maths',
                             participant_name='Bob, Sam')

    Music.participant_list_fk.append(Art_Music)
    DataBase.participant_list_fk.append(Computer_DataBase)
    Maths.participant_list_fk.append(Science_Maths)
    Sales.participant_list_fk.append(Business_Sales)
    Maths.participant_list_fk.append(Math_Maths)

    Art = Topic(topic_name='Art'
                )
    Science = Topic(topic_name='Science'
                    )
    Math = Topic(topic_name='Math'
                 )
    Computer = Topic(topic_name='Computer'
                     )
    Business = Topic(topic_name='Business'
                     )

    Sales.topic.append(Business)
    DataBase.topic.append(Computer)
    Music.topic.append(Art)
    Maths.topic.append(Science)
    Maths.topic.append(Math)

    db.session.add_all([Alex, Maria, Bob, Kate, Sam,
                        Sales, DataBase, Music, Math, Sports,
                        Science_Maths, Art_Music, Computer_DataBase, Business_Sales, Math_Maths,
                        Art, Science, Math, Computer, Business])

    db.session.commit()

    return render_template('index.html')



@app.route('/edit_user/<string:email>', methods=['GET', 'POST'])
@login_required
def edit_user(email):
    form = UserFormEdit()
    result = db.session.query(User).filter(User.user_email == email).one()

    if request.method == 'GET':

        form.user_name.data = result.user_name
        form.user_email.data = result.user_email
        form.user_birthday.data = result.user_birthday
        form.user_phone.data = result.user_phone

        return render_template('edit_user.html', form=form, form_name=email)
    elif request.method == 'POST':
        # if not form.validate():
        #     return render_template('edit_user.html', form=form, form_name=email)
        # else:

            result.user_name = form.user_name.data
            result.user_email = form.user_email.data
            result.user_birthday = form.user_birthday.data.strftime("%Y-%m-%d"),
            result.user_phone = form.user_phone.data

            db.session.commit()
            return redirect('/user')


@app.route('/edit_presentation/<string:name>', methods=['GET', 'POST'])
@login_required
def edit_presentation(name):
    form = PresentationFormEdit()
    result = db.session.query(Presentation).filter(Presentation.presentation_name == name).one()

    if request.method == 'GET':

        form.presentation_name.data = result.presentation_name
        form.presentation_date.data = result.presentation_date

        return render_template('edit_presentation.html', form=form, form_name=name)
    elif request.method == 'POST':
        if not form.validate():
            return render_template('edit_presentation.html', form=form, form_name=name)
        else:
            result.presentation_name = form.presentation_name.data
            result.presentation_date = form.presentation_date.data.strftime("%Y-%m-%d"),

            db.session.commit()
            return redirect('/presentation')


@app.route('/edit_topic/<string:name>', methods=['GET', 'POST'])
@login_required
def edit_topic(name):
    form = TopicFormEdit()
    result = db.session.query(Topic).filter(Topic.topic_name == name).one()

    if request.method == 'GET':

        form.topic_name.data = result.topic_name

        return render_template('edit_topic.html', form=form, form_name='Edit Topic')
    elif request.method == 'POST':
        if not form.validate():
            return render_template('edit_topic.html', form=form, form_name='Edit Topic')
        else:

            result.topic_name = form.topic_name.data

            db.session.commit()
            return redirect('/topic')


@app.route('/edit_participant/<string:name>', methods=['GET', 'POST'])
@login_required
def edit_participant(name):
    form = ParticipantFormEdit()
    result = db.session.query(Participant).filter(Participant.participant_list == name).one()

    if request.method == 'GET':

        form.participant_list.data = result.participant_list
        form.participant_name.data = result.participant_name

        return render_template('edit_participant.html', form=form, form_name='Edit Participant')
    elif request.method == 'POST':
        if not form.validate():
            return render_template('edit_participant.html', form=form, form_name='Edit Participant')
        else:
            result.participant_list = form.participant_list.data
            result.participant_name = form.participant_name.data

            db.session.commit()
            return redirect('/participant')


@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form = UserForm()

    if request.method == 'POST':
        # if not form.validate():
        #     return render_template('create_user.html', form=form)
        # else:
            count = db.session.query(User).filter(User.user_email == form.user_email.data).one_or_none()

            if count == None:
                roles = db.session.query(ormRole).filter(ormRole.name == "User").one()
                new_user = user_datastore.create_user(
                    username=form.user_name.data,
                    password=form.password.data,
                    email=form.user_email.data,
                    user_email=form.user_email.data,
                    user_name=form.user_name.data,
                    user_phone=form.user_phone.data,
                    user_birthday=form.user_birthday.data.strftime("%Y-%m-%d")
                    )
                new_user.roles.append(roles)
                db.session.add(new_user)
                db.session.commit()
                return redirect('/user')
            else:
                return render_template('create_user.html', form=form, error="User already exist")
    elif request.method == 'GET':
        return render_template('create_user.html', form=form)


@app.route('/delete_user/<string:email>', methods=['GET', 'POST'])
@login_required
def delete_user(email):
    result = db.session.query(User).filter(User.user_email == email).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/user')


@app.route('/create_topic', methods=['POST', 'GET'])
@login_required
def create_topic():
    form = TopicForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('create_topic.html', form=form)
        else:
            new_topic = Topic(
                topic_name=form.topic_name.data,
            )
            db.session.add(new_topic)
            db.session.commit()
            return redirect('/topic')
    elif request.method == 'GET':
        return render_template('create_topic.html', form=form)


@app.route('/delete_topic/<string:name>', methods=['GET', 'POST'])
@login_required
def delete_topic(name):
    result = db.session.query(Topic).filter(Topic.topic_name == name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/topic')


@app.route('/create_presentation', methods=['POST', 'GET'])
@login_required
def create_presentation():
    form = PresentationForm()
    users = db.session.query(User.user_email, User.user_name).all()
    form.user_email.choices = users
    if request.method == 'POST':
        if not form.validate():
            return render_template('create_presentation.html', form=form)
        else:
            count = db.session.query(Presentation).filter(
                Presentation.presentation_name == form.presentation_name.data).one_or_none()

            if count == None:
                new_topic = db.session.query(Topic).filter(Topic.topic_name == form.topic.data).one_or_none()
                if new_topic == None:
                    new_topic = Topic(
                        topic_name=form.topic.data
                    )

                email = db.session.query(User).filter(
                    User.user_email == form.user_email.data).one()
                new_presentation = Presentation(
                    presentation_name=form.presentation_name.data,
                    presentation_date=form.presentation_date.data.strftime("%Y-%m-%d"),
                    presentation_link=form.presentation_link.data
                )
                email.user_presentation.append(new_presentation)
                new_presentation.topic.append(new_topic)

                db.session.add(new_presentation)
                db.session.commit()
                return redirect('/presentation')
            else:
                return render_template('create_presentation.html', form=form, error="Presentation already exist")
    elif request.method == 'GET':

        return render_template('create_presentation.html', form=form)


@app.route('/delete_presentation/<string:name>', methods=['GET', 'POST'])
@login_required
def delete_presentation(name):
    result = db.session.query(Presentation).filter(Presentation.presentation_name == name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/presentation')


@app.route('/create_participant', methods=['POST', 'GET'])
@login_required
def create_participant():
    form = ParticipantForm()
    presentations_name = db.session.query(Presentation.presentation_name, Presentation.presentation_name).all()
    form.presentation_name.choices = presentations_name

    if request.method == 'POST':
        if not form.validate():
            return render_template('create_participant.html', form=form)
        else:
            count = db.session.query(Participant).filter(
                Participant.participant_list == form.participant_list.data).one_or_none()
            if count == None:
                new_participant = Participant(
                    participant_list=form.participant_list.data,
                    participant_name=form.participant_name.data
                )
                presentation_name = db.session.query(Presentation).filter(
                    Presentation.presentation_name == form.presentation_name.data).one()
                presentation_name.participant_list_fk.append(new_participant)
                db.session.add(new_participant)
                db.session.commit()
                return redirect('/participant')
            else:

                return render_template('create_participant.html', form=form)
    elif request.method == 'GET':
        return render_template('create_participant.html', form=form)


@app.route('/delete_participant/<string:name>', methods=['GET', 'POST'])
@login_required
def delete_participant(name):
    result = db.session.query(Participant).filter(Participant.participant_list == name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/participant')


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/user', methods=['GET'])
@login_required
def all_peolpe():
    if current_user.has_role('Admin'):
        result = db.session.query(User).all()
    else:
        result = db.session.query(User).filter(User.id == current_user.id).all()
    return render_template('all_user.html', result=result)


@app.route('/topic', methods=['GET'])
@login_required
def all_topic():
    result = db.session.query(Topic).all()

    return render_template('all_topic.html', result=result)


@app.route('/presentation', methods=['GET'])
@login_required
def all_presentation():
    result = db.session.query(Presentation).all()

    return render_template('all_presentation.html', result=result)


@app.route('/participant', methods=['GET'])
@login_required
def all_participant():
    result = db.session.query(Participant).all()

    return render_template('all_participant.html', result=result)


@app.route('/clustering', methods=['GET', 'POST'])
@app.route('/clustering/<title>', methods=['GET', 'POST'])
@login_required
def claster(title=None):
    dict = {}
    res1 = db.session.query(associations).all()
    for i in range(len(res1)):
        # if len(res1[i].topic) > 0:
        if res1[i][1] in dict:
            dict[res1[i][1]] += 1
        else:
            dict[res1[i][1]] = 1
    # pop = db.session.query(db.func.count()).filter(ormHashtags.hashtag_name == hashtag_name).one()[0]

    liste = []
    normal = {}
    unpopular = []
    popular = []
    k = 0
    for i in dict.keys():
        normal[k] = i
        k += 1

    pop = dict[title]

    k = 0
    for i in dict.keys():
        liste.append([])
        liste[k].append(dict[i])
        liste[k].append(k)
        k += 1
    matrix_data = np.matrix(liste)
    df = pd.DataFrame(matrix_data, columns=('par1', 'result'))
    print(df)
    X = df
    print(X)
    count_clasters = 2
    print(count_clasters)
    kmeans = KMeans(n_clusters=count_clasters, random_state=0).fit(X)
    # print(kmeans)
    count_columns = len(X.columns)
    iter = 0
    count_elements = [0, 0]
    for i in matrix_data:
        if kmeans.predict(i)[0] == 0:
            count_elements[0] += 1
            unpopular.append([normal[iter], dict[normal[iter]]])
        else:
            count_elements[1] += 1
            popular.append([normal[iter], dict[normal[iter]]])
        iter += 1

    pie = go.Pie(
        values=np.array(count_elements),
        labels=np.array(['unpopular', 'popular'])
    )
    data = {
        "pie": [pie]
    }

    input_list = []
    for i in range(1):
        input_list.append(Input_L)

    image_list = []
    for i in range(len(unpopular)):
        image_list.append(Image_L([unpopular[i][1]]))
    for i in range(len(popular)):
        image_list.append(Image_L([popular[i][1]]))

    class_A = Add_L()
    class_B = Add_L()

    res = Output_L()

    y_input = []
    y_image = []
    y_add = {}

    for i in range(1):
        y_input.append(input_list[i].activation(input_list[i], pop))

    y_image.append([])
    y_image.append([])
    for i in range(len(unpopular)):
        y_image[0].append(image_list[i].activation(y_input))
    for i in range(len(unpopular) + len(popular)):
        y_image[1].append(image_list[i].activation(y_input))

    y_add.update({"popular": class_A.activation(y_image[0])})
    y_add.update({"unpopular": class_B.activation(y_image[1])})

    res = res.activation(y_add)

    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('clasteresation.html', count_claster=count_clasters, graphsJSON=graphsJSON,
                           populatin="Teg " + title + " is " + res)


@app.route('/correlation', methods=['GET', 'POST'])
@login_required
def correlation():
    result_1 = db.session.query(Participant.participant_name, Participant.presentation_name).all()
    # result_2 = db.session.query(ormHashtags.hashtag_views).filter(ormHashtags.hashtag_name == hashtag_name).one()

    dict = {}
    for i in range(len(result_1)):
        # if len(res1[i].topic) > 0:
        if result_1[i][1] in dict:
            dict[result_1[i][1]] += len(result_1[i][0].split(", "))
        else:
            dict[result_1[i][1]] = len(result_1[i][0].split(", "))

    normal = {}
    k = 0
    for i in dict.keys():
        normal[i] = k
        k += 1
    k = 0
    liste = []
    for i in result_1:
        liste.append([])
        liste[k].append(dict[i[1]])
        liste[k].append(normal[i[1]])
        k += 1
    print(liste)

    matrix_data = np.matrix(liste)  # .transpose()

    df = pd.DataFrame(matrix_data, columns=('par1', 'result'))

    print(df)

    scaler = StandardScaler()
    scaler.fit(df[['par1']])
    train_X = scaler.transform(df[['par1']])
    # print(train_X, df[["count_files"]])
    reg = LinearRegression().fit(train_X, df[["result"]])

    test_array = [[liste[-1][0]]]
    test = scaler.transform(test_array)
    result = reg.predict(test)

    return render_template('regretion.html', row=int(round(result[0, 0])), test_data=test_array[0],
                           coef=reg.coef_[0],
                           coef1=reg.intercept_, error=None)

@app.route('/all/<topic>', methods=['GET', 'POST'])
@login_required
def all(topic):
    result = db.session.query(Presentation).join(associations).join(Topic).\
        filter(Presentation.presentation_name == associations.c.left_name).\
        filter(associations.c.right_name == Topic.topic_name).\
        filter(Topic.topic_name == topic).all()

    return render_template('all_presentation.html', result=result)

if __name__ == "__main__":
    app.run()
