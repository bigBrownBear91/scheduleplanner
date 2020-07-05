from flask import Blueprint, render_template, url_for, request, redirect

from myapp.database_helpers import query_teams, query_leagues, query_gamedates, update_gamedates
from myapp.models import GameDate
from myapp import db
from myapp.forms import UpdateGameDate
from myapp.helpers import ValuesQuerystring

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

        guest_game_form = UpdateGameDate()
        guest_game_form.home_team.data = second_team.name
        guest_game_form.guest_team.data = schedule_for_team.name

        return render_template('scheduleplanner.html', home_game_form=home_game_form, guest_game_form=guest_game_form)


@view_bp.route('/scheduleplanner', methods=['POST'])
def update_gamedates_from_scheduleplanner():
    vqs = ValuesQuerystring(request.headers.get('Referer'))
    team = query_teams(team_id=vqs.schedule_for_team)
    update_gamedates()
    return 'some'
    # return redirect(url_for('view_bp.get_scheduleplanner_page', second_team_id=None, schedule_for_team=team.id))

