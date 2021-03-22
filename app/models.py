
from collections import defaultdict
import random
from typing import List, Tuple
from .modules import (
    Inflexion,

    Inflect,
    Inflection,
    Inflector,
    LemmInflect,
    NLTK,
    Pattern,
    PyInflect,
    TextBlob,

    Module,
)
from .constants import CONVERSIONS, POS, Wordform

MODULES = [
    Inflexion,

    Inflect,
    Inflection,
    Inflector,
    LemmInflect,
    NLTK,
    Pattern,
    PyInflect,
    TextBlob,
]

MODULE_NAMES = [module().get_name() for module in MODULES]

SUPPORTED_WORDFORMS = {
    POS.N: [Wordform.SING, Wordform.PLUR],
    POS.V: [Wordform.SING, Wordform.PLUR, Wordform.PAST, Wordform.PAST_PART, Wordform.PRES_PART],
    POS.A: [Wordform.SING, Wordform.PLUR],
}

SUPPORTED_MODULES = defaultdict(lambda: defaultdict(list))
for module_class in MODULES:
    module = module_class()
    for pos in [POS.N, POS.V, POS.A]:
        for wordform in SUPPORTED_WORDFORMS[pos]:
            try:
                module.run(pos, wordform, "")
            except NotImplementedError:
                continue
            except Exception:
                pass
            SUPPORTED_MODULES[pos][wordform].append(module_class)


def get_random_conversion() -> Tuple[str, str]:
    """
    Return an arbitrarily chosen conversion, i.e. a POS and Wordform.
    """
    return random.choice(CONVERSIONS)


def is_lemma_form(pos: str, wordform: str) -> bool:
    """
    True iff the given Wordform represents the Lemma form of the given pos,
    i.e. plural for verbs, singular for nouns and either for adjectives.
    """
    return (pos == POS.V and wordform == Wordform.PLUR) or \
           (pos == POS.N and wordform == Wordform.SING) or \
           (pos == POS.A and wordform in (Wordform.SING, Wordform.PLUR))


def get_supported_modules(pos: str, wordform: str, show_competitors: bool) -> List[Module]:
    """
    Return the list of classes which support the conversion to `wordform` for the given `pos`.
    If `show_competitors` is False, the list can only contain Inflexion.
    """
    module_classes = SUPPORTED_MODULES[pos][wordform]
    return [module for module in module_classes 
            if show_competitors or module == Inflexion]


"""
_pos_wordform_to_method = {
    POS.V:
    {
        Wordform.SING: lambda mod: mod.verb_to_singular,
        Wordform.PLUR: lambda mod: mod.verb_to_plural,
        "past": lambda mod: mod.verb_to_pret,
        "past_part": lambda mod: mod.verb_to_past_part,
        "pres_part": lambda mod: mod.verb_to_pres_part
    },
    POS.N:
    {
        Wordform.SING: lambda mod: mod.noun_to_singular,
        Wordform.PLUR: lambda mod: mod.noun_to_plural,
    },
    "a":
    {
        Wordform.SING: lambda mod: mod.adj_to_singular,
        Wordform.PLUR: lambda mod: mod.adj_to_plural,
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
