from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField
from wtforms import validators


class UserFormEdit(FlaskForm):
    user_name = StringField("Name: ", [validators.Length(2, 20, "Name should be from 2 to 20 symbols")])
    user_email = HiddenField("Email: ", [validators.Email("Wrong email format")])
    user_birthday = DateField("Birthday: ")
    user_phone = IntegerField("Phone: ",  [validators.DataRequired("Please enter your phone."),
                                         validators.number_range(1000000000, 999999999999, "Phone should be from 10 to 12 symbols")])


    submit = SubmitField("Save")