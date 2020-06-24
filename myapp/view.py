from flask import Blueprint, render_template

from myapp.queries import query_teams, query_leagues

view_bp = Blueprint('view_bp', __name__, template_folder='templates')


@view_bp.route('/', methods=['GET'])
def get_index_page():
    league = query_leagues(league_name='NLB')
    all_leagues = query_leagues(all_entries=True)
    teams = query_teams(league_id=league.id)

    return render_template('index.html', leagues=all_leagues, teams=teams)


@view_bp.route('/scheduleplanner', methods=['GET'])
def get_scheduleplanner_page():
    return render_template('scheduleplanner.html')
