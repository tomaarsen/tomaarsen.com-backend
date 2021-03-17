from collections import defaultdict
from sys import breakpointhook
from flask import Flask, request, render_template, send_from_directory, url_for, render_template, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000")

# Initialize MongoDB database
client = pymongo.MongoClient("localhost:27017")
db = client["AGID"]

POS = ["v", "n", "a"]
WORDFORMS = ['sing', 'plur', 'past', 'past_part', 'pres_part']

pos_wordform_to_method = {
    "v":
    {
        "sing": lambda mod: mod.verb_to_singular,
        "plur": lambda mod: mod.verb_to_plural,
        "past": lambda mod: mod.verb_to_pret,
        "past_part": lambda mod: mod.verb_to_past_part,
        "pres_part": lambda mod: mod.verb_to_pres_part
    },
    "n":
    {
        "sing": lambda mod: mod.noun_to_singular,
        "plur": lambda mod: mod.noun_to_plural,
    },
    "a":
    {
        "sing": lambda mod: mod.adj_to_singular,
        "plur": lambda mod: mod.adj_to_plural,
    },
}

module_name_to_module = {
    "Inflexion": Inflexion,

    "inflect": Inflect,
    "Inflection": Inflection,
    "Inflector": Inflector,
    "LemmInflect": LemmInflect,
    "NLTK": NLTK,
    "Pattern": Pattern,
    "PyInflect": PyInflect,
    "TextBlob": TextBlob,
}

pos_wordform_to_modules = {}
for pos in POS:
    pos_wordform_to_modules[pos] = {}
    for wordform in WORDFORMS:
        # Check if this pos/wordform combination is legal
        try:
            method_lambda = pos_wordform_to_method[pos][wordform]
        except KeyError:
            continue

        pos_wordform_to_modules[pos][wordform] = []
        for modulename, module in module_name_to_module.items():
            # Get the method, and run it with an empty string, and detect if there is a NotImplementedError
            try:
                method = method_lambda(module())
                method("")
            except NotImplementedError:
                continue
            except Exception as e:
                pass
            # If we reach here, then there is no NotImplementedError (but perhaps another error).
            pos_wordform_to_modules[pos][wordform].append(modulename)


def get_module_names(pos, wordform, show_competitors):
    module_names = pos_wordform_to_modules[pos][wordform]
    if show_competitors:
        return module_names
    if "Inflexion" in module_names:
        return ["Inflexion"]
    return []


"""
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html', modules=list(module_name_to_module.keys()))


@app.route("/<path>", methods=["GET"])
def redirect_to_index(path):
    return redirect("/", code=302)
"""

"""
@socketio.on('connect')
def test_connect():
    emit('after connect', {'data': 'Lets dance'})


@socketio.on('random')
def emit_random_output(json):
    # show_competitors = json["show_competitors"]

    conversions = [
        ("n", "sing"),
        ("n", "plur"),
        ("v", "sing"),
        ("v", "plur"),
        ("v", "past"),
        ("v", "pres_part"),
        ("v", "past_part")
    ]
    pos, wordform = random.choice(conversions)
    emit_modules({**json, **{
        "pos": pos,
        "wordform": wordform
    }})
    # TODO: Ensure that the Database cannot be empty.
    try:
        word_entry = db[f"{pos.upper()}_to_word"].aggregate(
            [{"$sample": {"size": 1}}]).next()
    except StopIteration:
        return
    word = random.choice(list(word_entry.values()))
    if isinstance(word, list):
        word = word[0]
    emit("conversion", {
        "pos": pos,
        "wordform": wordform,
        "word": word
    })
    emit_output({**json, **{
        "pos": pos,
        "wordform": wordform,
        "word": word
    }})


@socketio.on("input")
def emit_output(json):
    print("Input", json)
    pos = json["pos"]
    wordform = json["wordform"]
    word = json["word"]
    show_competitors = json["show_competitors"]

    # If known, get known correct output
    # First get lemma of the given word
    if pos != "a":
        lemma_entry = db[f"{pos.upper()}_to_lemma"].find_one({"_id": word})
        if lemma_entry:
            lemma = lemma_entry["lemma"]

            # Check if we are converting to the lemma
            if (pos == "v" and wordform == "plur") or \
                (pos == "n" and wordform == "sing") or \
                    (pos == "a" and wordform == "plur"):
                emit("correct", {
                    "output": [lemma]
                })
            else:
                # Otherwise use the to_word database to potentially find a word
                # in the desired wordform
                word_entry = db[f"{pos.upper()}_to_word"].find_one({
                    "_id": lemma})
                if wordform in word_entry:
                    correct_words = list(word_entry[wordform])
                elif wordform == "past_part" and "past" in word_entry:
                    correct_words = list(word_entry["past"])
                else:
                    breakpoint()
                emit("correct", {
                    "output": correct_words
                })

    module_names = get_module_names(pos, wordform, show_competitors)
    for module_name in module_names:
        module = module_name_to_module[module_name]()
        method = pos_wordform_to_method[pos][wordform](module)
        output = method(word)
        emit("output", {
            "module": module_name,
            "output": output
        })


@socketio.on("input_modules")
def emit_modules(json):
    print("Input_modules", json)
    pos = json["pos"]
    wordform = json["wordform"]
    show_competitors = json["show_competitors"]
    module_names = get_module_names(pos, wordform, show_competitors)
    emit("output_modules", {
        "modules": module_names
    })
"""

'''
@app.errorhandler(404)
def page_not_found(e):
    """Handle error gracefully"""
    return jsonify({"msg": "Resource not found. Visit API docs for more info.", "type": "+OK", "return": None})
    # return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle internal server error gracefully"""
    return jsonify({"msg": "Internal server error. Please contact support.", "type": "+OK", "return": None})
'''

if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=5000, debug=True)
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)

# TODO: Adjective
# TODO: on-hover to explain source of results
# TODO: Refresh is buggy
