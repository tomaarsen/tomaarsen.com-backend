
from collections import defaultdict
import random
import json
from typing import List, Tuple
from .modules import (
    Inflex,
    Module,
)
from .constants import (
    POS,
    Wordform, 
    CONVERSIONS,
    SUPPORTED_MODULES
)

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
    If `show_competitors` is False, the list can only contain Inflex.
    """
    module_classes = SUPPORTED_MODULES[pos][wordform]
    return [module for module in module_classes
            if show_competitors or module == Inflex]


def get_performance(pos: str, wordform: str, source: str):
    """
    Given a `pos` and `wordform`, return the list of modules that support the corresponding conversion,
    also return a dictionary mapping wordforms to a list of accuracies. Each accuracy score corresponds
    to a module in the list of modules
    """
    sources = {
        "celex": "app/static/data/celex_performance.json",
        "celex_word": "app/static/data/celex_word_performance.json",
        "celex_collocation": "app/static/data/celex_collocation_performance.json",
        "agid": "app/static/data/agid_performance.json",
        "wiktionary": "app/static/data/wiktionary_performance.json",
        "wiktionary_word": "app/static/data/wiktionary_word_performance.json",
        "wiktionary_collocation": "app/static/data/wiktionary_collocation_performance.json",
    }
    with open(sources[source], "r") as f:
        data = json.load(f)
        performance_dict = data[pos][wordform]
        module_names = list(next(data.keys() for data in performance_dict.values()))
        n_terms = sum(performance_dict[list(performance_dict.keys())[0]][module_names[0]].values())
        return module_names, {
            key: [performance_dict[key][module]["correct"] * 100 / (performance_dict[key][module]["correct"] + performance_dict[key][module]["incorrect"]) for module in module_names]
            for key in performance_dict
        }, n_terms