from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import import DataRequired, Email, EqualTo
from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password',validators=[DataRequired()])

    Submit = SubmitField('Login')

Class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField ('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirmation', message='Passwords not matching')])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired()])
    Submit = SubmitField('Register')

    def check_email(self,field):
        if User,query.filter_by(email=field.data).first():
            raise ValidationError('email already reqistered')

    def check_username(self,field):
        if User,query.filter_by(username=field.data).first():
            raise ValidationError('username already excist')
