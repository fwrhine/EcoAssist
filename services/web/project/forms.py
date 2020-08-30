from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    details = TextAreaField('Details')
    reason = TextAreaField('Why this task?')
    points = IntegerField('Points', validators=[DataRequired()])
    class_id = SelectField('Assign to', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Create')
