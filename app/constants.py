
from collections import defaultdict
from .models import (
    Inflex,
    Inflect,
    Inflection,
    Inflector,
    LemmInflect,
    NLTK,
    Pattern,
    PyInflect,
    TextBlob,
)

class POS:
    V = "v"
    N = "n"
    A = "a"

class Wordform:
    SING = 'sing'
    PLUR = 'plur'
    PAST = 'past'
    PAST_PART = 'past_part'
    PRES_PART = 'pres_part'
    COMP = 'comp'
    SUPER = 'super'

CONVERSIONS = [
    (POS.N, Wordform.SING),
    (POS.N, Wordform.PLUR),
    
    (POS.V, Wordform.SING),
    (POS.V, Wordform.PLUR),
    (POS.V, Wordform.PAST),
    (POS.V, Wordform.PRES_PART),
    (POS.V, Wordform.PAST_PART),
    
    (POS.A, Wordform.SING),
    (POS.A, Wordform.PLUR),
    (POS.A, Wordform.COMP),
    (POS.A, Wordform.SUPER),
]

MODULES = [
    Inflex,

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
    POS.A: [Wordform.SING, Wordform.PLUR, Wordform.COMP, Wordform.SUPER],
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