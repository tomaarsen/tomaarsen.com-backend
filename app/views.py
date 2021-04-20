from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from .models import MODULE_NAMES

bp = Blueprint("inflex", __name__, url_prefix="/inflex",
               static_folder="static/css")

@bp.route("/")
def index():
    return redirect(url_for("inflex.inflex_try"), code=302)

@bp.route("/try")
def inflex_try():
    return render_template("inflex/try.html", modules=MODULE_NAMES)

@bp.route("/performance")
def inflex_performance():
    return render_template("inflex/performance.html")

# @bp.route("/test")
# def test():
    # return render_template("inflex/test.html")

@bp.route("/<path>")
def redirect_to_index(path):
    print(path)
    return redirect(url_for("inflex.inflex_try"), code=302)
