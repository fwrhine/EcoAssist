import os

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, PasswordField, BooleanField, RadioField
from wtforms.validators import DataRequired, InputRequired, Email, ValidationError
from .models import User, TeacherClasses
from wtforms.fields.html5 import DateField


app = Flask(__name__)
app.config.from_object("project.config.Config")


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    details = TextAreaField('Details')
    points = IntegerField('Points', validators=[DataRequired()])
    resource_id = SelectField(
        'Theme', coerce=int, validators=[InputRequired()])
    class_id = SelectField('For Class', coerce=int,
                           validators=[InputRequired()])
    required_approval = BooleanField('Requires Approval')

    submit = SubmitField('Create')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    class_code = StringField('Class Code')
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate(self):
        if self.email.data and self.password.data:
            user = User.query.filter_by(email=self.email.data).first()
            if user is None:
                self.email.errors += (ValidationError("Email is not registered"),)
                return False
            else:
                check_password = User.query.filter_by(
                    email=self.email.data, password=self.password.data).first()
                if check_password is None:
                    self.password.errors += (ValidationError("Wrong password"),)
                    return False
        else:
            if not self.email.data:
                self.email.errors += (ValidationError("This field is required"),)
            if not self.password.data:
                self.password.errors += (ValidationError("This field is required"),)
            return False
        return True


class ClassForm(FlaskForm):
    class_name = StringField('Class Name', validators=[DataRequired()])
    submit = SubmitField('Create')


class StudentClassForm(FlaskForm):
    class_code = StringField('Class Code', validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_class_code(self, class_code):
        print("check")
        teacher_classes = TeacherClasses.query.filter_by(
            class_code=class_code.data).first()
        print(teacher_classes)
        if teacher_classes is None:
            print("doesnt")
            raise ValidationError("Class doesn't exist")

class AwardForm(FlaskForm):
    # class_id = StringField('Class Name', validators=[DataRequired()])
    student_names = SelectField('Student', coerce=int,
                           validators=[InputRequired()])
    reward = StringField('Title', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])

    images_dir = os.listdir(os.path.join(app.static_folder, "images/badge_images"))
    choices = []
    for x in images_dir:
        value = x
        label = x
        choices.append((value, label))

    images = RadioField('Badges', choices=choices)
    submit = SubmitField('Create')

class ChooseClassForm(FlaskForm):
    class_id = SelectField('For Class', coerce=int,
                           validators=[InputRequired()])
    submit = SubmitField('Confirm')
