
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