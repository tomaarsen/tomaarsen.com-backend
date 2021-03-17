from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('inflexion', __name__, url_prefix='/inflexion',
               static_folder="static")

module_name_to_module = [
    "Inflexion",
    "inflect",
    "Inflection",
    "Inflector",
    "LemmInflect",
    "NLTK",
    "Pattern",
    "PyInflect",
    "TextBlob",
]


@bp.route('/')
def index():
    return render_template('index.html', modules=module_name_to_module)


@bp.route("/<path>")
def redirect_to_index(path):
    return redirect(url_for("inflexion.index"), code=302)
