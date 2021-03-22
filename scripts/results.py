
import pandas as pd
import json
from pprint import pprint

with open("Scripts/results.json", "r") as f:
    out = json.load(f)


v = out["V"]
n = out["N"]
verb_results = {
    to_wordform: {
        from_wordform: {
            module: results["correct"] / (results["correct"] + results["incorrect"]) * 100
            for module, results in v[to_wordform][from_wordform].items()
        }
        for from_wordform in v[to_wordform]
    }
    for to_wordform in v
}
noun_results = {
    to_wordform: {
        from_wordform: {
            module: results["correct"] / (results["correct"] + results["incorrect"]) * 100
            for module, results in n[to_wordform][from_wordform].items()
        }
        for from_wordform in n[to_wordform]
    }
    for to_wordform in n
}

past = pd.DataFrame(verb_results["past"])
plur = pd.DataFrame(verb_results["plur"])
sing = pd.DataFrame(verb_results["sing"])
past_part = pd.DataFrame(verb_results["past_part"])
pres_part = pd.DataFrame(verb_results["pres_part"])

nplur = pd.DataFrame(noun_results["plur"])
nsing = pd.DataFrame(noun_results["sing"])

breakpoint()
