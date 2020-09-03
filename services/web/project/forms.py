from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Email, ValidationError
from .models import User


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
