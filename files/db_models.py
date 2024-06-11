from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    # Variables for user data
    id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    name = db.Column(db.String)
    active = db.Column(db.Boolean, default = True)

    def __init__(self, email, password, name = None, active = True):
        self.email = email
        self.password = password
        self.name = name
        self.active = active

class Notes(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    data = db.Column(db.String, nullable = False)
    time = db.Column(db.DateTime, default = func.current_date())

    def __init__(self, user_id, data):
        self.user_id = user_id
        self.data = data

class Registration(FlaskForm):
    name = StringField('Name', [validators.InputRequired(
                                message = "Please give us your name!"), 
                                validators.Length(min = 3)])
    
    email = StringField('E-mail', [validators.InputRequired(
                                   message = "Please input your e-mail!"),
                                   validators.Length(min = 5)])
    
    password = PasswordField('Password', 
                        [validators.Length(min = 8, 
                         message = "Password must be at least 8 characters long!"), 
                         validators.Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', 
                         message = "*Use at least 8 characters: digits, uppercase, lowercase and special characters!"),
                         validators.InputRequired(
                         message = "Please input your password!"), 
                         validators.EqualTo('confirm', 
                         message = "Passwords must match!")])
    
    confirm = PasswordField('Repeat Password')
    
    submit = SubmitField('Register!')

    def validate_email(self, email):
        if Users.query.filter_by(email = email.data).first():
            raise ValidationError('E-mail already in use.')

class Login(FlaskForm):
    
    email = StringField('E-mail', [validators.InputRequired(message = "Please input your e-mail!")])
    
    password = PasswordField('Password', [validators.InputRequired(message = "Please input your password!")])
    
    submit = SubmitField('Log in!')
    
    
