from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField, SelectField
from wtforms.validators import DataRequired

import myapp.database_handlers as db_handlers


class UpdateGameDate(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    pool = StringField('Pool', validators=[DataRequired()])
    home_team = StringField('Hometeam')
    guest_team = StringField('Guestteam')


class UpdateTeam(FlaskForm):
    name = StringField('Name', validators=[])
    person = StringField('Person', validators=[])
    pool = StringField('Pool', validators=[])
    league = StringField('Liga', validators=[])
    submit = SubmitField('Submit')


class InsertTeam(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    person = StringField('Person')
    pool = StringField('Pool')
    league = SelectField('League', validate_choice=False,
                         choices=[league.name for league in db_handlers.query_leagues(all_entries=True)])
    club = StringField('Club', validators=[DataRequired()])
    submit = SubmitField('Submit')


class InsertClub(FlaskForm):
    existing_clubs = SelectField('Existing Clubs', validate_choice=False,
                                 choices=['None'] + [club.name for club in db_handlers.query_clubs(all_entries=True)])
    name = StringField('Name')
    submit = SubmitField('Submit')
