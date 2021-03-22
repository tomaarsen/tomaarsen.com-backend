from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from .models import MODULE_NAMES

bp = Blueprint('inflexion', __name__, url_prefix='/inflexion',
               static_folder="static")

@bp.route('/')
def index():
    return render_template('index.html', modules=MODULE_NAMES)


@bp.route("/<path>")
def redirect_to_index(path):
    return redirect(url_for("inflexion.index"), code=302)
