from flask import Blueprint, render_template, url_for, request

from myapp.queries import query_teams, query_leagues, query_gamedates
from myapp.models import GameDate
from myapp import db

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
    league = query_leagues(league_id=schedule_for_team.league_id)
    all_teams_of_league = query_teams(league_id=league.id)
    all_teams_of_league.remove(schedule_for_team)

    gamedates = []

    for second_team in all_teams_of_league:
        home_game = query_gamedates(schedule_for_team, second_team)
        away_game = query_gamedates(second_team, schedule_for_team)
        if home_game is not None:
            gamedates.append(home_game)
        else:
            new_gamedate = GameDate(None, None, None, schedule_for_team, second_team)
            db.session.add(new_gamedate)

        if away_game is not None:
            gamedates.append(away_game)
        else:
            new_gamedate = GameDate(None, None, None, second_team, schedule_for_team)
            db.session.add(new_gamedate)

        db.session.commit()

    return render_template('scheduleplanner.html', schedule_for_team=schedule_for_team, gamedates=gamedates)
