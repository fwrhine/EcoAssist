import os

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, PasswordField, RadioField
from wtforms.validators import DataRequired, InputRequired, Email, ValidationError
from wtforms.fields.html5 import DateField

from .models import User

app = Flask(__name__)
app.config.from_object("project.config.Config")


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    details = TextAreaField('Details')
    reason = TextAreaField('Why this task?')
    points = IntegerField('Points', validators=[DataRequired()])
    resource_id = SelectField(
        'Theme', coerce=int, validators=[InputRequired()])
    class_id = SelectField('For Class', coerce=int,
                           validators=[InputRequired()])
    submit = SubmitField('Create')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    class_code = StringField('Class Code')
    submit = SubmitField('Create')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ClassForm(FlaskForm):
    class_name = StringField('Class Name', validators=[DataRequired()])
    submit = SubmitField('Create')

class AwardForm(FlaskForm):
    # class_id = StringField('Class Name', validators=[DataRequired()])  
    student_names = SelectField('For Student', coerce=int,
                           validators=[InputRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d') 
    reward = StringField('Reward', validators=[DataRequired()])
    comment = StringField('Comments', validators=[DataRequired()])

    images_dir = os.listdir(os.path.join(app.static_folder, "badge_images"))
    choices = []
    for x in images_dir:
        value = x
        label = x
        choices.append((value, label))

    images = RadioField('image', choices=choices)
    submit = SubmitField('Create')

class ChooseClassForm(FlaskForm):
    class_id = SelectField('For Class', coerce=int,
                           validators=[InputRequired()])
    submit = SubmitField('Confirm')