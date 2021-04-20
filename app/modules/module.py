
from ..constants import POS, Wordform


class Module(object):
    def __init__(self) -> None:
        super().__init__()

    def run(self, pos: str, wordform: str, term: str, *args, **kwargs) -> str:
        if pos == POS.N:
            if wordform == Wordform.SING:
                return self.noun_to_singular(term, *args, **kwargs)
            elif wordform == Wordform.PLUR:
                return self.noun_to_plural(term, *args, **kwargs)

        elif pos == POS.V:
            if wordform == Wordform.SING:
                return self.verb_to_singular(term, *args, **kwargs)
            elif wordform == Wordform.PLUR:
                return self.verb_to_plural(term, *args, **kwargs)
            elif wordform == Wordform.PAST:
                return self.verb_to_pret(term, *args, **kwargs)
            elif wordform == Wordform.PAST_PART:
                return self.verb_to_past_part(term, *args, **kwargs)
            elif wordform == Wordform.PRES_PART:
                return self.verb_to_pres_part(term, *args, **kwargs)

        elif pos == POS.A:
            if wordform == Wordform.SING:
                return self.adj_to_singular(term, *args, **kwargs)
            elif wordform == Wordform.PLUR:
                return self.adj_to_plural(term, *args, **kwargs)
            elif wordform == Wordform.COMP:
                return self.adj_to_comparative(term, *args, **kwargs)
            elif wordform == Wordform.SUPER:
                return self.adj_to_superlative(term, *args, **kwargs)

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    # START OF NOUN
    # Conversions
    def noun_to_singular(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def noun_to_plural(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def noun_to_classical_plural(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    # Checking
    def noun_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def noun_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()
    # END OF NOUN

    # START OF VERB
    # Conversions
    def verb_to_singular(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_to_plural(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_to_pret(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_to_past_part(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_to_pres_part(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    # Checking
    def verb_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def verb_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def verb_is_pret(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_is_past_part(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_is_pres_part(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()
    # END OF VERB

    # START OF ADJECTIVE
    # Conversions
    def adj_to_singular(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def adj_to_plural(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    # Checking
    def adj_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def adj_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def adj_to_comparative(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def adj_to_superlative(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()
    # END OF ADJECTIVE
