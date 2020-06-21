#!/usr/bin/env python3
from flask import Flask

from myapp.models import db


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    if config is not None:
        app.config.from_pyfile(config)

    db.init_app(app)

    with app.app_context():
        import myapp.view
        app.register_blueprint(view.view_bp)

        return app
