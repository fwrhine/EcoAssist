from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError
from .models import User

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    school = StringField('School',validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')