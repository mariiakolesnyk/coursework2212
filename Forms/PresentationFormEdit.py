from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField
from wtforms import validators
from datetime import date
from wtforms_components import DateRange


class PresentationFormEdit(FlaskForm):
    presentation_name = HiddenField("Name: ", [validators.Length(2, 40, "Name should be from 2 to 40 symbols")])
    presentation_date = DateField("Date: ", [validators.DataRequired("Please enter date of presentation."),
                                             DateRange(min=date(1900, 1, 1),max=date(2400, 1, 1))])
    presentation_link = StringField("Link: ",[
                                  # validators.DataRequired("Please enter name of presentation."),
                                  validators.Length(5, 500, "Link should be from 2 to 40 symbols")
                                  ])

    submit = SubmitField("Save")