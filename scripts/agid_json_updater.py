
import json

with open("backup/agid.json") as f:
    agid = json.load(f)

def rm_id(entry):
    del entry["_id"]
    return entry

agid = {
    "a": {
        "to_word": {entry["_id"]: rm_id(entry) for entry in agid["a"]["to_word"]},
        "to_lemma": {entry["_id"]: entry["lemma"] for entry in agid["a"]["to_lemma"]}
    },
    "n": {
        "to_word": {entry["_id"]: rm_id(entry) for entry in agid["n"]["to_word"]},
        "to_lemma": {entry["_id"]: entry["lemma"] for entry in agid["n"]["to_lemma"]}
    },
    "v": {
        "to_word": {entry["_id"]: rm_id(entry) for entry in agid["v"]["to_word"]},
        "to_lemma": {entry["_id"]: entry["lemma"] for entry in agid["v"]["to_lemma"]}
    },
}

with open("agid_json/agid.json", "w") as f:
    json.dump(agid, f)
# breakpoint()
