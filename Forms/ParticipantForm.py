from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms import validators


class ParticipantForm(FlaskForm):
    participant_list = StringField("List name: ", [
        validators.DataRequired("Please enter participants list name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    participant_name = StringField("Participant name: ", [
        validators.DataRequired("Please enter participant name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    presentation_name = SelectField('Presentation')

    submit = SubmitField("Save")