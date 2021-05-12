from app.db import get_known_corrects, get_random_word_lemma
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import time
import random

from .models import MODULE_NAMES, get_performance, get_random_conversion, get_supported_modules

# bp = Blueprint("inflex", __name__, url_prefix="/inflex")

# @bp.route("/")
# def index():
#     return redirect(url_for("inflex.inflex_try"), code=302)

# @bp.route("/try")
# def inflex_try():
#     return render_template("inflex/try.html", modules=MODULE_NAMES)

# @bp.route("/performance")
# def inflex_performance():
#     return render_template("inflex/performance.html")

# # @bp.route("/test")
# # def test():
#     # return render_template("inflex/test.html")

# @bp.route("/<path>")
# def redirect_to_index(path):
#     print(path)
#     return redirect(url_for("inflex.inflex_try"), code=302)

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/try/go", methods=["POST"])
def api_try():
    # Get request parameters
    pos = request.json["pos"]
    wordform = request.json["wordform"]
    word = request.json["word"]
    show_competitors = request.json["show_competitors"]

    known_corrects = get_known_corrects(pos, wordform, word)
    modules = get_supported_modules(pos, wordform, show_competitors)
    answers = []
    for module in modules:
        output = module().run(pos, wordform, word)
        answers.append({
            "module": module.get_name(),
            "output": output
        })
    return jsonify({
        "known_corrects": known_corrects,
        "answers": answers
    })


@api.route("/try/random", methods=["POST"])
def api_try_random():
    show_competitors = request.json["show_competitors"]

    # Get a random conversion
    pos, wordform = get_random_conversion()

    # Get a random word
    word, lemma = get_random_word_lemma(pos)

    known_corrects = get_known_corrects(pos, wordform, lemma)
    modules = get_supported_modules(pos, wordform, show_competitors)
    answers = []
    for module in modules:
        output = module().run(pos, wordform, word)
        answers.append({
            "module": module.get_name(),
            "output": output
        })
    return jsonify({
        "pos": pos,
        "wordform": wordform,
        "word": word,
        "known_corrects": known_corrects,
        "answers": answers
    })


@api.route("/try/modules", methods=["POST"])
def api_try_modules():
    # Get request parameters
    pos = request.json["pos"]
    wordform = request.json["wordform"]
    show_competitors = request.json["show_competitors"]

    # Emit the list of modules that support the desired conversion
    print([module.get_name()
           for module in get_supported_modules(pos, wordform, show_competitors)])
    return jsonify({
        "modules": [module.get_name()
                    for module in get_supported_modules(pos, wordform, show_competitors)]
    })


@api.route("/performance", methods=["POST"])
def api_performance():
    # Get request parameters
    pos = request.json["pos"]
    wordform = request.json["wordform"]
    source = request.json["source"]

    labels, performance, n_terms = get_performance(pos, wordform, source)

    return jsonify({
        "labels": labels,
        "performance": performance,
        "n_terms": n_terms
    })
