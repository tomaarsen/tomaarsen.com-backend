import os

from flask import Flask, redirect, url_for
import eventlet
from flask_socketio import SocketIO

from .socket import InflexionNamespace

socketio = SocketIO(cors_allowed_origins="http://127.0.0.1:5000")

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import views
    app.register_blueprint(views.bp)

    @app.errorhandler(404)
    def page_not_found(e):
        """Redirect to inflexion for the time being"""
        return redirect(url_for("inflexion.index"), 302)

    socketio.init_app(app)
    socketio.on_namespace(InflexionNamespace())

    return app
