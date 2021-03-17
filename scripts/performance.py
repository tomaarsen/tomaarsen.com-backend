
from modules import (Inflect,
                     Inflection,
                     Inflector,
                     Inflexion,
                     LemmInflect,
                     NLTK,
                     Pattern,
                     PyInflect,
                     TextBlob,
                     )
import pymongo
from pprint import pprint
import json

client = pymongo.MongoClient("localhost:27017")
db = client["AGID"]

id_to_lemma = {
    "V": "plur",
    "N": "sing",
    "A": "plur", # ?
}

pos_wordform_to_method = {
    "V":
    {
        "sing": lambda mod: mod.verb_to_singular,
        "plur": lambda mod: mod.verb_to_plural,
        "past": lambda mod: mod.verb_to_pret,
        "past_part": lambda mod: mod.verb_to_past_part,
        "pres_part": lambda mod: mod.verb_to_pres_part
    },
    "N":
    {
        "sing": lambda mod: mod.noun_to_singular,
        "plur": lambda mod: mod.noun_to_plural,
    },
    "A":
    {
        "sing": lambda mod: mod.adj_to_singular,
        "plur": lambda mod: mod.adj_to_plural,
    },
}

modules = [
    Inflexion(),
    Inflect(),
    Inflection(),
    Inflector(),
    LemmInflect(),
    NLTK(),
    Pattern(),
    PyInflect(),
    TextBlob(),
]

results = {}
for pos in ["V", "N"]:
    print("Starting with ", pos)
    results[pos] = {}
    cursor = db[f"{pos}_to_word"].find({})

    total = cursor.count()
    last_percentage = 1
    for i, document in enumerate(cursor):
        document[id_to_lemma[pos]] = [document["_id"]]
        del document["_id"]
        if pos == "V" and "past_part" not in document:
            document["past_part"] = document["past"]
        for to_wordform, to_words in document.items():
            if to_wordform not in results[pos]:
                results[pos][to_wordform] = {}
            for from_wordform, from_words in document.items():
                if from_wordform not in results[pos][to_wordform]:
                    results[pos][to_wordform][from_wordform] = {}
                for module in modules:
                    method = pos_wordform_to_method[pos][to_wordform](module)
                    try:
                        for from_word in from_words:
                            output = method(from_word)
                            if module.__class__.__name__ not in results[pos][to_wordform][from_wordform]:
                                results[pos][to_wordform][from_wordform][module.__class__.__name__] = {"correct": 0, "incorrect": 0}
                            if output in to_words:
                                results[pos][to_wordform][from_wordform][module.__class__.__name__]["correct"] += 1
                            else:
                                results[pos][to_wordform][from_wordform][module.__class__.__name__]["incorrect"] += 1
                    except NotImplementedError:
                        pass
        
        pct = i / total * 100
        if round(pct) > last_percentage:
            print(f"{pct:.2f}%")
            last_percentage = round(pct)

breakpoint()
with open("results.json") as f:
    json.dump(results, f)
breakpoint()
