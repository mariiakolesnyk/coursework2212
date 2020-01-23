from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms import validators


class TopicFormEdit(FlaskForm):
    topic_name = StringField("Topic: ", [
        validators.DataRequired("Please enter presentation topic."),
        validators.Length(2, 40, "Topic should be from 2 to 40 symbols")
    ])

    submit = SubmitField("Save")