from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField, SelectField
from wtforms import validators


class ParticipantFormEdit(FlaskForm):
    participant_list = StringField("List name: ", [validators.Length(3, 20, "Name should be from 3 to 20 symbols")])
    participant_name = StringField("Participant name: ", [validators.Length(3, 20, "Name should be from 3 to 20 symbols")])

    submit = SubmitField("Save")