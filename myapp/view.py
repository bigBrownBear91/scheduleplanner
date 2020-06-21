from flask import Blueprint, render_template

view_bp = Blueprint('view_bp', __name__, template_folder='templates')


@view_bp.route('/', methods=['GET'])
def get_index_page():
    return render_template('index.html')
