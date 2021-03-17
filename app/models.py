
"""
_pos_wordform_to_method = {
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

def get_method(pos: str, wordform: str):
    return _pos_wordform_to_method[pos][wordform]

def get_module_names(pos: str, wordform: str, show_competitors: bool):
    module_names = pos_wordform_to_modules[pos][wordform]
    if show_competitors:
        return module_names
    if "Inflexion" in module_names:
        return ["Inflexion"]
    return []
"""