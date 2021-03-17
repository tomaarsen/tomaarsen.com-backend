
__all__ = [
    "LemmInflect"
]
from .module import Module

from pyinflect import getInflection

# https://github.com/bjascob/pyInflect
class PyInflect(Module):

    # START OF NOUN
    # Conversions
    def noun_to_singular(self, term: str, *args, **kwargs) -> str:
        o = getInflection(term, tag="NN")
        if o:
            return o[0]
        return None

    def noun_to_plural(self, term: str, *args, **kwargs) -> str:
        o = getInflection(term, tag="NNS")
        if o:
            return o[0]
        return None

    def noun_to_classical_plural(self, term: str, *args, **kwargs) -> str:
        o = getInflection(term, tag="NNS")
        if o:
            return o[-1]
        return None

    # Checking
    def noun_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def noun_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()
    # END OF NOUN

    # START OF VERB
    # Conversions
    def verb_to_singular(self, term: str, *args, **kwargs) -> str:
        o = getInflection(term, tag="VBZ")
        if o:
            return o[0]
        return None

    def verb_to_plural(self, term: str, *args, **kwargs) -> str:
        o = getInflection(term, tag="VB")
        if o:
            return o[0]
        return None

    def verb_to_pret(self, term: str, *args, **kwargs) -> str:
        o = getInflection(term, tag="VBD")
        if o:
            return o[0]
        return None

    def verb_to_past_part(self, term: str, *args, **kwargs) -> str:
        o = getInflection(term, tag="VBN")
        if o:
            return o[0]
        return None

    def verb_to_pres_part(self, term: str, *args, **kwargs) -> str:
        o = getInflection(term, tag="VBG")
        if o:
            return o[0]
        return None

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
    # END OF ADJECTIVE
