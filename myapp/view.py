from flask import Blueprint, render_template, url_for, request, redirect

from myapp.database_handlers import query_teams, query_leagues, query_gamedates, update_gamedates, query_pools, \
    query_clubs, update_team_instance
from myapp.models import GameDate
from myapp import db
from myapp.forms import UpdateGameDate, UpdateTeam
from myapp.helpers import StringToDate, StringToTime, ValuesQuerystring

view_bp = Blueprint('view_bp', __name__, template_folder='templates')


@view_bp.route('/', methods=['GET'])
def get_index_page():
    league = query_leagues(league_name='NLB')
    all_leagues = query_leagues(all_entries=True)
    teams = query_teams(league_id=league.id)

    return render_template('index.html', leagues=all_leagues, teams=teams)


@view_bp.route('/scheduleplanner', methods=['GET'])
def get_scheduleplanner_page():
    schedule_for_team_id = request.args.get('schedule_for_team')
    schedule_for_team = query_teams(team_id=schedule_for_team_id)
    second_team_id = request.args.get('second_team_id')

    if second_team_id is None:
        league = query_leagues(league_id=schedule_for_team.league_id)
        all_teams_of_league = query_teams(league_id=league.id)
        all_teams_of_league.remove(schedule_for_team)

        gamedates = []

        for second_team in all_teams_of_league:
            gamedates.append({'home_team': schedule_for_team, 'guest_team': second_team})

        return render_template('scheduleplanner.html', second_team_id=None, schedule_for_team=schedule_for_team,
                               gamedates=gamedates)

    else:
        second_team = query_teams(team_id=second_team_id)
        home_game = query_gamedates(schedule_for_team, second_team)
        guest_game = query_gamedates(second_team, schedule_for_team)

        home_game_form = UpdateGameDate()
        home_game_form.home_team.data = schedule_for_team.name
        home_game_form.guest_team.data = second_team.name
        if home_game.date is not None:
            home_game_form.date.data = home_game.date
        if home_game.time is not None: home_game_form.time.data = home_game.time
        if home_game.pool is not None: home_game_form.pool.data = home_game.pool.name
        home_game_form.home_team.id = 'home_hometeam'
        home_game_form.guest_team.id = 'home_guestteam'
        home_game_form.date.id = 'home_date'
        home_game_form.time.id = 'home_time'
        home_game_form.pool.id = 'home_pool'

        guest_game_form = UpdateGameDate()
        guest_game_form.home_team.data = second_team.name
        guest_game_form.guest_team.data = schedule_for_team.name
        if guest_game.date is not None: guest_game_form.date.data = guest_game.date
        if guest_game.time is not None: guest_game_form.time.data = guest_game.time
        if guest_game.pool is not None: guest_game_form.pool.data = guest_game.pool.name
        guest_game_form.home_team.id = 'guest_hometeam'
        guest_game_form.guest_team.id = 'guest_guestteam'
        guest_game_form.date.id = 'guest_date'
        guest_game_form.time.id = 'guest_time'
        guest_game_form.pool.id = 'guest_pool'

        return render_template('scheduleplanner.html', home_game_form=home_game_form, guest_game_form=guest_game_form)


@view_bp.route('/scheduleplanner', methods=['POST'])
def update_gamedates_from_scheduleplanner():
    update_gamedate_form = request.form
    schedule_for_team = query_teams(team_name=update_gamedate_form['home_hometeam'])
    second_team = query_teams(team_name=update_gamedate_form['home_guestteam'])
    # "home" refers to the team that is scheduling his games while "guest" means the other team
    home_pool = query_pools(pool_name=update_gamedate_form['home_pool'])
    away_pool = query_pools(pool_name=update_gamedate_form['guest_pool'])

    # Update homegame
    update_gamedates(schedule_for_team, second_team, StringToDate(update_gamedate_form['home_date']).date_as_date,
                     StringToTime(update_gamedate_form['home_time']).time_as_time, home_pool)
    # Update away game
    update_gamedates(second_team, schedule_for_team, StringToDate(update_gamedate_form['guest_date']).date_as_date,
                     StringToTime(update_gamedate_form['guest_time']).time_as_time, away_pool)

    return redirect(url_for('view_bp.get_scheduleplanner_page', second_team_id=None,
                            schedule_for_team=schedule_for_team.id))


@view_bp.route('/all_teams', methods=['GET'])
def get_allteams():
    clubs = query_clubs(all_entries=True)
    return render_template('all_teams.html', clubs=clubs)


@view_bp.route('/update_team', methods=['GET', 'POST'])
def update_team():
    update_team_form = UpdateTeam(request.form)
    vqs = ValuesQuerystring(request.url)

    if request.method == 'GET':
        team = query_teams(team_id=vqs.team_id)
        update_team_form.name.data = team.name
        if team.person:
            update_team_form.person.data = team.person.name
        if team.pool:
            update_team_form.pool.data = team.pool.name
        update_team_form.league.data = team.league.name
        return render_template('/update_team.html', team=team, update_team=update_team_form)

    elif update_team_form.validate_on_submit():
        update_values = {k: update_team_form.data[k] for k in update_team_form.data if k in ['name', 'person', 'pool', 'league']}
        update_team_instance(team_id=vqs.team_id, **update_values)
        return redirect(url_for('view_bp.get_allteams'))

    else:
        raise Exception(f'request.method is {request.method}\nform is submitted: {update_team_form.is_submitted()}\n'
                        f'form is valid: {update_team_form.validate()}')
