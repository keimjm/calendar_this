import imp
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, DateField, StringField, SubmitField, TextAreaField, TimeField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

class AppointmentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    start_date = DateField("Start", validators=[DataRequired()])
    start_time = TimeField("Start", validators=[DataRequired()])
    end_date = DateField("End", validators=[DataRequired()])
    end_time = TimeField("End", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    private = BooleanField("Private")
    submit = SubmitField("Submit")

    def validate_end_date(form, field):
        start = datetime.combine(form.start_date.data, form.start_time.data)
        end = datetime.combine(field.data, form.end_time.data)
        if start >= end:
            msg = "End date/time must come after start date/time"
            raise ValidationError(msg)
        if start.day != end.day:
            msg ="End date must be same as start date"
            raise ValidationError(msg)