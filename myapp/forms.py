from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField
from wtforms.validators import DataRequired


class UpdateGameDate(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    pool = StringField('Pool', validators=[DataRequired()])
    home_team = StringField('Hometeam')
    guest_team = StringField('Guestteam')
