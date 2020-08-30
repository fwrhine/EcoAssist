from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    details = TextAreaField('Details')
    reason = TextAreaField('Why this task?')
    points = IntegerField('Points', validators=[DataRequired()])
    submit = SubmitField('Create')
